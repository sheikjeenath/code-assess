"""
Scoring service for CodeAssess.

Computes a single weighted overall score from test-case correctness,
AI-reported code quality, complexity, readability, and interview readiness.
"""

import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Complexity score lookup table
# O-notation string -> score (0-100)
# ---------------------------------------------------------------------------
_COMPLEXITY_SCORE_MAP: dict[str, int] = {
    "o(1)": 100,
    "o(log n)": 90,
    "o(n)": 80,
    "o(n log n)": 70,
    "o(n^2)": 50,
    "o(n2)": 50,       # alternative notation
    "o(n²)": 50,       # unicode superscript variant
    "o(2^n)": 20,
    "o(2n)": 20,       # alternative notation
    "o(n!)": 10,
}

_DEFAULT_COMPLEXITY_SCORE = 60  # used when the notation is not in the table

# ---------------------------------------------------------------------------
# Weight constants (must sum to 1.0)
# ---------------------------------------------------------------------------
_W_CORRECTNESS = 0.5
_W_CODE_QUALITY = 0.2
_W_COMPLEXITY = 0.1
_W_READABILITY = 0.1
_W_OPTIMIZATION = 0.1


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _safe_get_quality_scores(ai_report: dict) -> dict:
    """Return the qualityScores dict from ai_report, with safe fallback."""
    try:
        scores = ai_report.get("qualityScores", {})
        if isinstance(scores, dict):
            return scores
    except Exception:
        pass
    return {}


def _safe_get_interview_score(ai_report: dict) -> float:
    """Return interviewFeedback.interviewScore as a float, defaulting to 50."""
    try:
        feedback = ai_report.get("interviewFeedback", {})
        if isinstance(feedback, dict):
            score = feedback.get("interviewScore", 50)
            return float(score)
    except Exception:
        pass
    return 50.0


def _safe_get_time_complexity(ai_report: dict) -> str:
    """Return the time complexity string from ai_report, or empty string."""
    try:
        complexity = ai_report.get("complexity", {})
        if isinstance(complexity, dict):
            return str(complexity.get("time", "")).strip()
    except Exception:
        pass
    return ""


def _complexity_to_score(time_complexity: str) -> int:
    """
    Map a Big-O time complexity string to a numeric score.

    Matching is case-insensitive and tolerates whitespace.
    Returns _DEFAULT_COMPLEXITY_SCORE for unrecognised notations.
    """
    normalised = time_complexity.lower().replace(" ", "")
    return _COMPLEXITY_SCORE_MAP.get(normalised, _DEFAULT_COMPLEXITY_SCORE)


def _average_quality_scores(quality_scores: dict) -> float:
    """
    Compute the mean of all numeric values in the qualityScores dict.

    Returns 50.0 if the dict is empty or contains no numeric values.
    """
    if not quality_scores:
        return 50.0

    numeric_values = []
    for v in quality_scores.values():
        try:
            numeric_values.append(float(v))
        except (TypeError, ValueError):
            pass

    if not numeric_values:
        return 50.0

    return sum(numeric_values) / len(numeric_values)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_overall_score(
    passed_cases: int,
    total_cases: int,
    ai_report: dict,
) -> dict:
    """
    Compute a weighted overall score combining correctness and AI analysis.

    Parameters
    ----------
    passed_cases : int
        Number of test cases the submission passed.
    total_cases : int
        Total number of test cases evaluated.
    ai_report : dict
        The structured AI analysis report returned by ai_service.analyze_code().

    Returns
    -------
    dict with keys:
        overallScore   (int)   - final rounded weighted score (0-100)
        scoreBreakdown (dict)  - per-dimension value + weight used in calculation

    The scoreBreakdown contains:
        correctness   {value: float, weight: 0.5}
        codeQuality   {value: float, weight: 0.2}
        complexity    {value: int,   weight: 0.1}
        readability   {value: float, weight: 0.1}
        optimization  {value: float, weight: 0.1}
    """
    if ai_report is None:
        ai_report = {}

    # ------------------------------------------------------------------
    # 1. Correctness  (test-case pass rate, 0-100)
    # ------------------------------------------------------------------
    try:
        if total_cases > 0:
            correctness = (passed_cases / total_cases) * 100.0
        else:
            correctness = 0.0
        correctness = max(0.0, min(100.0, correctness))
    except Exception:
        logger.warning("Could not compute correctness score; defaulting to 0.")
        correctness = 0.0

    # ------------------------------------------------------------------
    # 2. Code quality  (mean of all qualityScores dimensions, 0-100)
    # ------------------------------------------------------------------
    quality_scores = _safe_get_quality_scores(ai_report)
    code_quality = _average_quality_scores(quality_scores)

    # ------------------------------------------------------------------
    # 3. Complexity score  (mapped from time complexity string, 0-100)
    # ------------------------------------------------------------------
    time_complexity_str = _safe_get_time_complexity(ai_report)
    complexity_score = (
        _complexity_to_score(time_complexity_str)
        if time_complexity_str
        else _DEFAULT_COMPLEXITY_SCORE
    )

    # ------------------------------------------------------------------
    # 4. Readability  (qualityScores.readability, 0-100)
    # ------------------------------------------------------------------
    try:
        readability = float(quality_scores.get("readability", 50))
        readability = max(0.0, min(100.0, readability))
    except (TypeError, ValueError):
        readability = 50.0

    # ------------------------------------------------------------------
    # 5. Optimization  (interviewFeedback.interviewScore, 0-100)
    # ------------------------------------------------------------------
    optimization = _safe_get_interview_score(ai_report)
    optimization = max(0.0, min(100.0, optimization))

    # ------------------------------------------------------------------
    # Weighted combination
    # ------------------------------------------------------------------
    overall = (
        correctness   * _W_CORRECTNESS
        + code_quality  * _W_CODE_QUALITY
        + complexity_score * _W_COMPLEXITY
        + readability   * _W_READABILITY
        + optimization  * _W_OPTIMIZATION
    )

    overall_rounded = max(0, min(100, round(overall)))

    logger.debug(
        "Score breakdown -> correctness=%.1f, codeQuality=%.1f, complexity=%d, "
        "readability=%.1f, optimization=%.1f => overall=%d",
        correctness, code_quality, complexity_score,
        readability, optimization, overall_rounded,
    )

    return {
        "overallScore": overall_rounded,
        "scoreBreakdown": {
            "correctness": {
                "value": round(correctness, 2),
                "weight": _W_CORRECTNESS,
            },
            "codeQuality": {
                "value": round(code_quality, 2),
                "weight": _W_CODE_QUALITY,
            },
            "complexity": {
                "value": complexity_score,
                "weight": _W_COMPLEXITY,
            },
            "readability": {
                "value": round(readability, 2),
                "weight": _W_READABILITY,
            },
            "optimization": {
                "value": round(optimization, 2),
                "weight": _W_OPTIMIZATION,
            },
        },
    }
