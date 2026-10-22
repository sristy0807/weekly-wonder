
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


CONFIG = {
    "lookback_days": 7,
    "display_limit": 10,
    "database_path": "news.db",
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


def filter_recent_articles(articles, now, days=7):
    """Keep valid articles published within the time window."""
    cutoff = now - timedelta(days=days)
    filtered = []

    for article in articles:
        title = article.get("title", "").strip()
        url = article.get("url", "").strip()

        if not title or not url:
            continue

        try:
            published_at = datetime.fromisoformat(
                article["published_at"]
            )
        except (KeyError, TypeError, ValueError):
            continue

        # Interpret timestamps without timezone info as UTC.
        if published_at.tzinfo is None:
            published_at = published_at.replace(
                tzinfo=timezone.utc
            )

        if cutoff <= published_at <= now:
            filtered.append(article)

    return filtered


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


def collect_news(feeds):
    """Collect articles from all configured feeds."""
    collected = []

    for source_name, feed_url in feeds.items():
        try:
            articles = fetch_feed(source_name, feed_url)
            collected.extend(articles)

            print(f"{source_name}: fetched {len(articles)} articles")

        except (requests.RequestException, ValueError) as error:
            print(f"{source_name}: failed — {error}")

    return collected


def filter_news(articles, now, lookback_days=7):
    """Keep valid articles published within the configured date range."""
    cutoff = now - timedelta(days=lookback_days)
    filtered = []

    for article in articles:
        title = article.get("title", "").strip()
        url = article.get("url", "").strip()

        if not title or not url:
            continue

        try:
            published_at = datetime.fromisoformat(
                article["published_at"]
            )
        except (KeyError, TypeError, ValueError):
            continue

        if published_at.tzinfo is None:
            published_at = published_at.replace(
                tzinfo=timezone.utc
            )

        if cutoff <= published_at <= now:
            filtered.append(article)

    return filtered


def save_news(articles, database_path):
    """Initialize the database and save collected articles."""
    with sqlite3.connect(database_path) as connection:
        initialize_database(connection)
        inserted = save_articles(connection, articles)

    return inserted


def get_recent_news(now, lookback_days, database_path):
    """Retrieve articles within the configured date range."""
    cutoff = now - timedelta(days=lookback_days)

    with sqlite3.connect(database_path) as connection:
        rows = connection.execute("""
            SELECT title, source, published_at, url
            FROM articles
            WHERE published_at >= ?
              AND published_at <= ?
            ORDER BY published_at DESC
        """, (
            cutoff.isoformat(),
            now.isoformat(),
        )).fetchall()

    return rows


def display_news(rows, inserted, display_limit=10):
    """Display a summary and the most recent articles."""
    print(f"\nNew articles saved: {inserted}")
    print(f"Recent articles in database: {len(rows)}")

    for title, source, published_at, url in rows[:display_limit]:
        print(f"\n[{source}] {title}")
        print(f"Published: {published_at}")
        print(url)



def main(config=None):
    """Orchestrate the Weekly Wonder collection workflow."""
    config = config or CONFIG
    now = datetime.now(timezone.utc)

    collected = collect_news(FEEDS)

    filtered = filter_news(
        collected,
        now,
        lookback_days=config["lookback_days"],
    )

    inserted = save_news(
        filtered,
        database_path=config["database_path"],
    )

    recent_news = get_recent_news(
        now,
        lookback_days=config["lookback_days"],
        database_path=config["database_path"],
    )

    display_news(
        recent_news,
        inserted,
        display_limit=config["display_limit"],
    )


if __name__ == "__main__":
    main()
