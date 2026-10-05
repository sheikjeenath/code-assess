"""
Gemini AI service for CodeAssess.

Provides code analysis using Google Gemini (gemini-1.5-flash).
Loads prompt templates from Firestore (aiPrompts collection, where active==True)
and falls back to a hardcoded default when none is found.
"""

import json
import logging
import re

import google.generativeai as genai

from config import Config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Gemini SDK initialisation
# ---------------------------------------------------------------------------
genai.configure(api_key=Config.GEMINI_API_KEY)

_GEMINI_MODEL = "gemini-1.5-flash"

# ---------------------------------------------------------------------------
# Default prompt template (used when no Firestore template is active)
# ---------------------------------------------------------------------------
_DEFAULT_PROMPT_TEMPLATE = """You are an expert software engineer and code reviewer specialising in {language}.

You are evaluating a candidate's solution to the following coding problem:

**Problem Title:** {problem_title}

**Problem Description:**
{problem_description}

**Candidate's Code ({language}):**
```
{code}
```

Analyse the code thoroughly and respond with ONLY a single raw JSON object — no markdown, no code fences, no extra text before or after. The JSON must conform exactly to this structure:

{{
  "qualityScores": {{
    "readability": <integer 0-100>,
    "naming": <integer 0-100>,
    "design": <integer 0-100>,
    "modularity": <integer 0-100>,
    "maintainability": <integer 0-100>,
    "bestPractices": <integer 0-100>,
    "errorHandling": <integer 0-100>
  }},
  "scoreExplanations": {{
    "readability": "<concise explanation>",
    "naming": "<concise explanation>",
    "design": "<concise explanation>",
    "modularity": "<concise explanation>",
    "maintainability": "<concise explanation>",
    "bestPractices": "<concise explanation>",
    "errorHandling": "<concise explanation>"
  }},
  "complexity": {{
    "time": "O(...)",
    "space": "O(...)",
    "justification": "<brief justification>",
    "optimizations": "<suggested optimizations or 'None'>"
  }},
  "explanation": "<plain English walkthrough of what the code does step by step>",
  "flowchartMermaid": "graph TD\\n  A[Start] --> ...",
  "improvedCode": "<optimised rewrite of the code in {language}>",
  "improvementExplanation": "<what changed and why>",
  "interviewFeedback": {{
    "interviewReady": "<Yes|Partial|No>",
    "verdictSummary": "<one or two sentence overall verdict>",
    "likelyFollowUpQuestions": ["<question 1>", "<question 2>", "<question 3>"],
    "betterApproach": "<description of a better approach if one exists, or 'This is already optimal'>",
    "interviewScore": <integer 0-100>
  }}
}}
"""

# ---------------------------------------------------------------------------
# Error response skeleton
# ---------------------------------------------------------------------------
_ERROR_QUALITY_SCORES = {
    "readability": 50,
    "naming": 50,
    "design": 50,
    "modularity": 50,
    "maintainability": 50,
    "bestPractices": 50,
    "errorHandling": 50,
}

_ERROR_SCORE_EXPLANATIONS = {
    "readability": "Analysis unavailable.",
    "naming": "Analysis unavailable.",
    "design": "Analysis unavailable.",
    "modularity": "Analysis unavailable.",
    "maintainability": "Analysis unavailable.",
    "bestPractices": "Analysis unavailable.",
    "errorHandling": "Analysis unavailable.",
}


def _build_error_report(error_message: str) -> dict:
    """Return a fully-structured dict (all required keys present) describing a failed analysis."""
    return {
        "qualityScores": _ERROR_QUALITY_SCORES.copy(),
        "scoreExplanations": _ERROR_SCORE_EXPLANATIONS.copy(),
        "complexity": {
            "time": "O(n)",
            "space": "O(n)",
            "justification": "Analysis unavailable due to an error.",
            "optimizations": "Analysis unavailable.",
        },
        "explanation": f"AI analysis failed: {error_message}",
        "flowchartMermaid": "graph TD\n  A[Start] --> B[Error]",
        "improvedCode": "// Analysis unavailable.",
        "improvementExplanation": f"AI analysis failed: {error_message}",
        "interviewFeedback": {
            "interviewReady": "No",
            "verdictSummary": f"Analysis could not be completed: {error_message}",
            "likelyFollowUpQuestions": [],
            "betterApproach": "Analysis unavailable.",
            "interviewScore": 50,
        },
    }


# ---------------------------------------------------------------------------
# Firestore prompt loader
# ---------------------------------------------------------------------------

def _load_prompt_template_from_firestore() -> str | None:
    """
    Query the Firestore `aiPrompts` collection for a document where active==True.

    Returns the `template` field string if found, or None if Firestore is
    unavailable or no active prompt exists.
    """
    try:
        # Import here to avoid hard dependency when Firestore is not configured
        from firebase_admin import firestore as fs

        db = fs.client()
        docs = (
            db.collection("aiPrompts")
            .where("active", "==", True)
            .limit(1)
            .stream()
        )
        for doc in docs:
            data = doc.to_dict()
            template = data.get("template")
            if template:
                logger.debug("Loaded active AI prompt template from Firestore (doc: %s).", doc.id)
                return template
    except Exception as exc:
        logger.warning("Could not load prompt template from Firestore: %s", exc)

    return None


def _get_prompt_template() -> str:
    """Return the active prompt template from Firestore, or the built-in default."""
    template = _load_prompt_template_from_firestore()
    if template:
        return template
    logger.debug("Using hardcoded default prompt template.")
    return _DEFAULT_PROMPT_TEMPLATE


# ---------------------------------------------------------------------------
# Markdown fence stripper
# ---------------------------------------------------------------------------

def _strip_markdown_fences(text: str) -> str:
    """
    Remove leading/trailing markdown code fences from a string.

    Handles variations like:
        ```json ... ```
        ``` ... ```
        `...`
    """
    # Strip leading/trailing whitespace first
    text = text.strip()

    # Remove fenced code block markers (```json, ```JSON, ```, etc.)
    text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
    text = re.sub(r"\n?```$", "", text)
    text = re.sub(r"^```[a-zA-Z]*", "", text)
    text = re.sub(r"```$", "", text)

    # Strip inline back-ticks (single) if the whole text is wrapped
    if text.startswith("`") and text.endswith("`"):
        text = text[1:-1]

    return text.strip()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_code(
    code: str,
    language: str,
    problem_title: str,
    problem_description: str,
) -> dict:
    """
    Analyse candidate code using Gemini and return a structured report.

    Parameters
    ----------
    code : str
        The candidate's source code.
    language : str
        Programming language name (e.g. "python", "java").
    problem_title : str
        Title of the coding problem.
    problem_description : str
        Full description of the coding problem.

    Returns
    -------
    dict
        A fully-populated analysis report with the following top-level keys:
        qualityScores, scoreExplanations, complexity, explanation,
        flowchartMermaid, improvedCode, improvementExplanation, interviewFeedback.
        On error, all keys are present but contain error messages.
    """
    template = _get_prompt_template()

    try:
        prompt = template.format(
            code=code,
            language=language,
            problem_title=problem_title,
            problem_description=problem_description,
        )
    except KeyError as exc:
        logger.error("Prompt template has unknown placeholder: %s", exc)
        # Fall back to default template
        prompt = _DEFAULT_PROMPT_TEMPLATE.format(
            code=code,
            language=language,
            problem_title=problem_title,
            problem_description=problem_description,
        )

    logger.debug("Sending code analysis request to Gemini (model=%s).", _GEMINI_MODEL)

    try:
        model = genai.GenerativeModel(_GEMINI_MODEL)
        gemini_response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                top_p=0.95,
                max_output_tokens=8192,
            ),
        )
    except Exception as exc:
        logger.error("Gemini API call failed: %s", exc)
        return _build_error_report(f"Gemini API error: {exc}")

    raw_text: str = ""
    try:
        raw_text = gemini_response.text
    except Exception as exc:
        logger.error("Could not extract text from Gemini response: %s", exc)
        return _build_error_report(f"Could not read Gemini response: {exc}")

    # Strip any markdown fences the model may have added despite instructions
    clean_text = _strip_markdown_fences(raw_text)

    try:
        report: dict = json.loads(clean_text)
    except json.JSONDecodeError as exc:
        logger.error(
            "JSON parse failed for Gemini response. Error: %s\nRaw text (first 500 chars): %s",
            exc,
            raw_text[:500],
        )
        return _build_error_report(
            f"JSON parsing failed ({exc}). Raw response snippet: {raw_text[:200]}"
        )

    # Ensure all required top-level keys are present; fill in defaults for any missing
    report.setdefault("qualityScores", _ERROR_QUALITY_SCORES.copy())
    report.setdefault("scoreExplanations", _ERROR_SCORE_EXPLANATIONS.copy())
    report.setdefault(
        "complexity",
        {"time": "O(n)", "space": "O(n)", "justification": "", "optimizations": ""},
    )
    report.setdefault("explanation", "")
    report.setdefault("flowchartMermaid", "graph TD\n  A[Start] --> B[End]")
    report.setdefault("improvedCode", code)
    report.setdefault("improvementExplanation", "")
    report.setdefault(
        "interviewFeedback",
        {
            "interviewReady": "Partial",
            "verdictSummary": "",
            "likelyFollowUpQuestions": [],
            "betterApproach": "",
            "interviewScore": 50,
        },
    )

    # Ensure qualityScores sub-keys are present
    quality_defaults = {
        "readability": 50, "naming": 50, "design": 50, "modularity": 50,
        "maintainability": 50, "bestPractices": 50, "errorHandling": 50,
    }
    for k, v in quality_defaults.items():
        report["qualityScores"].setdefault(k, v)

    # Ensure interviewFeedback sub-keys are present
    interview_defaults = {
        "interviewReady": "Partial",
        "verdictSummary": "",
        "likelyFollowUpQuestions": [],
        "betterApproach": "",
        "interviewScore": 50,
    }
    for k, v in interview_defaults.items():
        report["interviewFeedback"].setdefault(k, v)

    logger.debug("Gemini analysis complete.")
    return report
