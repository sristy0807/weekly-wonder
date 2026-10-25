"""Validated content ratings for Weekly Wonder stories."""

from dataclasses import dataclass
import math
from numbers import Real
from typing import Mapping


RATING_FACTORS = (
    "curiosity_gap",
    "broad_appeal",
    "emotional_activation",
    "story_depth",
    "consequence",
    "visual_concreteness",
)


@dataclass(frozen=True)
class FactorRating:
    """A single 0–10 score and its justification."""

    score: int | float
    explanation: str

    def __post_init__(self):
        if isinstance(self.score, bool) or not isinstance(self.score, Real):
            raise ValueError("score must be a number from 0 to 10")
        if not math.isfinite(self.score) or not 0 <= self.score <= 10:
            raise ValueError("score must be a finite number from 0 to 10")
        if not isinstance(self.explanation, str) or not self.explanation.strip():
            raise ValueError("explanation must be a non-empty string")


@dataclass(frozen=True)
class ContentRating:
    """Validated scores for all six content factors."""

    curiosity_gap: FactorRating
    broad_appeal: FactorRating
    emotional_activation: FactorRating
    story_depth: FactorRating
    consequence: FactorRating
    visual_concreteness: FactorRating

    def __post_init__(self):
        for factor in RATING_FACTORS:
            if not isinstance(getattr(self, factor), FactorRating):
                raise ValueError(f"{factor} must be a FactorRating")

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "ContentRating":
        """Build a rating from factor objects, rejecting missing or malformed data."""
        if not isinstance(data, Mapping):
            raise ValueError("rating must be a mapping of all six factors")

        missing = [factor for factor in RATING_FACTORS if factor not in data]
        if missing:
            raise ValueError(f"missing rating factors: {', '.join(missing)}")

        ratings = {}
        for factor in RATING_FACTORS:
            value = data[factor]
            if isinstance(value, FactorRating):
                ratings[factor] = value
            elif isinstance(value, Mapping):
                if "score" not in value or "explanation" not in value:
                    raise ValueError(
                        f"{factor} must include score and explanation"
                    )
                ratings[factor] = FactorRating(
                    score=value["score"],
                    explanation=value["explanation"],
                )
            else:
                raise ValueError(f"{factor} must include score and explanation")

        return cls(**ratings)

    @property
    def raw_overall_score(self) -> float:
        """Return the full precision normalized score on a 0–100 scale."""
        score_sum = sum(getattr(self, factor).score for factor in RATING_FACTORS)
        return (score_sum / 60) * 100

    @property
    def overall_score(self) -> float:
        """Return the normalized score rounded for display and serialization."""
        return round(self.raw_overall_score, 2)

    def to_dict(self) -> dict[str, object]:
        """Serialize factor scores and explanations with the displayed total."""
        result = {
            factor: {
                "score": getattr(self, factor).score,
                "explanation": getattr(self, factor).explanation,
            }
            for factor in RATING_FACTORS
        }
        result["overall_score"] = self.overall_score
        return result
