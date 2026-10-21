
import calendar
import sqlite3
from datetime import datetime, timedelta, timezone

import feedparser
import requests


FEEDS = {
    "OpenAI": "https://openai.com/news/rss.xml",
    "AI News": (
        "https://news.google.com/rss/search"
        "?q=artificial+intelligence"
        "&hl=en-US&gl=US&ceid=US:en"
    ),
}


def fetch_feed(source_name, feed_url):
    """Download and parse one RSS feed."""
    response = requests.get(
        feed_url,
        timeout=20,
        headers={"User-Agent": "WeeklyWonder/0.1"}
    )
    response.raise_for_status()

    parsed_feed = feedparser.parse(response.content)

    articles = []

    for entry in parsed_feed.entries:
        published = entry.get("published_parsed")

        # Skip entries without a usable publication date.
        if published is None:
            continue

        published_at = datetime.fromtimestamp(
            calendar.timegm(published),
            tz=timezone.utc
        )

        articles.append({
            "title": entry.get("title", "").strip(),
            "url": entry.get("link", "").strip(),
            "source": source_name,
            "published_at": published_at.isoformat(),
        })

    return articles


def initialize_database(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            url TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            source TEXT NOT NULL,
            published_at TEXT NOT NULL
        )
    """)
    connection.commit()


def save_articles(connection, articles):
    """Insert new articles; ignore links already stored."""
    before = connection.total_changes

    connection.executemany("""
        INSERT OR IGNORE INTO articles
            (url, title, source, published_at)
        VALUES
            (:url, :title, :source, :published_at)
    """, articles)

    connection.commit()
    return connection.total_changes - before


def main():
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=7)
    collected = []

    for source_name, feed_url in FEEDS.items():
        try:
            articles = fetch_feed(source_name, feed_url)

            recent_articles = [
                article for article in articles
                if article["url"]
                and article["title"]
                and cutoff <= datetime.fromisoformat(
                    article["published_at"]
                ) <= now
            ]

            collected.extend(recent_articles)

            print(
                f"{source_name}: "
                f"{len(recent_articles)} recent articles"
            )

        except (requests.RequestException, ValueError) as error:
            print(f"{source_name}: failed — {error}")

    with sqlite3.connect("news.db") as connection:
        initialize_database(connection)
        inserted = save_articles(connection, collected)

        rows = connection.execute("""
            SELECT title, source, published_at, url
            FROM articles
            WHERE published_at >= ?
            ORDER BY published_at DESC
        """, (cutoff.isoformat(),)).fetchall()

    print(f"\nNew articles saved: {inserted}")
    print(f"Recent articles in database: {len(rows)}")

    for title, source, published_at, url in rows[:10]:
        print(f"\n[{source}] {title}")
        print(f"Published: {published_at}")
        print(url)


if __name__ == "__main__":
    main()
