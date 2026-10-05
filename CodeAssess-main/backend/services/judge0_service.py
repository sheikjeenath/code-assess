"""
Judge0 API client service for CodeAssess.

Handles code execution via Judge0 CE/Extra CE API with support for
Python, C++, Java, and JavaScript. Includes retry logic for queued
submissions and RapidAPI authentication when a key is configured.
"""

import base64
import time
import logging
from urllib.parse import urlparse

import requests

from config import Config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Language ID mapping (Judge0 language IDs)
# ---------------------------------------------------------------------------
LANGUAGE_IDS: dict[str, int] = {
    "python": 71,       # Python 3.8.1
    "cpp": 54,          # C++ (GCC 9.2.0)
    "java": 62,         # Java (OpenJDK 13.0.1)
    "javascript": 63,   # JavaScript (Node.js 12.14.0)
}

# Status IDs returned by Judge0
STATUS_IN_QUEUE = 1
STATUS_PROCESSING = 2
STATUS_ACCEPTED = 3
STATUS_WRONG_ANSWER = 4
STATUS_TIME_LIMIT_EXCEEDED = 5
STATUS_COMPILATION_ERROR = 6
STATUS_RUNTIME_ERROR_SIGSEGV = 11
STATUS_RUNTIME_ERROR_SIGXFSZ = 12
STATUS_RUNTIME_ERROR_SIGFPE = 13
STATUS_RUNTIME_ERROR_SIGABRT = 14
STATUS_RUNTIME_ERROR_NZEC = 15
STATUS_RUNTIME_ERROR_OTHER = 16

# Polling configuration
MAX_POLL_ATTEMPTS = 10
POLL_SLEEP_SECONDS = 1


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _encode(text: str) -> str:
    """Base64-encode a UTF-8 string for the Judge0 payload."""
    if text is None:
        return ""
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def _decode(b64_text) -> str:
    """Decode a base64 string returned by Judge0; return empty string if None."""
    if not b64_text:
        return ""
    try:
        return base64.b64decode(b64_text).decode("utf-8", errors="replace")
    except Exception:
        return b64_text  # return as-is if decode fails


def _build_headers(api_url: str, api_key) -> dict:
    """
    Build HTTP request headers.

    When an API key is provided, RapidAPI authentication headers are added.
    The RapidAPI host is extracted from the configured JUDGE0_API_URL hostname.
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if api_key:
        parsed = urlparse(api_url)
        rapid_host = parsed.hostname or ""
        headers["X-RapidAPI-Key"] = api_key
        headers["X-RapidAPI-Host"] = rapid_host
    return headers


def _map_status(status_id: int, status_description: str) -> str:
    """Map a Judge0 status_id to a human-readable status string used internally."""
    mapping = {
        STATUS_IN_QUEUE: "In Queue",
        STATUS_PROCESSING: "Processing",
        STATUS_ACCEPTED: "Accepted",
        STATUS_WRONG_ANSWER: "Wrong Answer",
        STATUS_TIME_LIMIT_EXCEEDED: "Time Limit Exceeded",
        STATUS_COMPILATION_ERROR: "Compilation Error",
        STATUS_RUNTIME_ERROR_SIGSEGV: "Runtime Error (SIGSEGV)",
        STATUS_RUNTIME_ERROR_SIGXFSZ: "Runtime Error (SIGXFSZ)",
        STATUS_RUNTIME_ERROR_SIGFPE: "Runtime Error (SIGFPE)",
        STATUS_RUNTIME_ERROR_SIGABRT: "Runtime Error (SIGABRT)",
        STATUS_RUNTIME_ERROR_NZEC: "Runtime Error (NZEC)",
        STATUS_RUNTIME_ERROR_OTHER: "Runtime Error",
    }
    return mapping.get(status_id, status_description or "Unknown")


def _parse_response(data: dict) -> dict:
    """
    Parse a Judge0 submission response dict and return a normalised result dict.

    Fields returned:
        stdout          - decoded standard output
        stderr          - decoded standard error
        compile_output  - decoded compiler output (non-empty on compile errors)
        status          - human-readable status string
        status_id       - raw integer status id
        runtime         - execution time in seconds (string) or empty string
        memory          - memory used in KB (integer) or None
    """
    status_obj = data.get("status") or {}
    status_id = status_obj.get("id", 0)
    status_description = status_obj.get("description", "")

    return {
        "stdout": _decode(data.get("stdout")),
        "stderr": _decode(data.get("stderr")),
        "compile_output": _decode(data.get("compile_output")),
        "status": _map_status(status_id, status_description),
        "status_id": status_id,
        "runtime": data.get("time") or "",
        "memory": data.get("memory"),
    }


def _poll_until_done(api_url: str, token: str, headers: dict) -> dict:
    """
    Poll Judge0 for a submission result until it leaves In Queue / Processing.

    Attempts up to MAX_POLL_ATTEMPTS times with POLL_SLEEP_SECONDS between each.
    Returns the last received response dict regardless of final status.
    """
    get_url = f"{api_url}/submissions/{token}?base64_encoded=true"
    last_data: dict = {}

    for attempt in range(1, MAX_POLL_ATTEMPTS + 1):
        time.sleep(POLL_SLEEP_SECONDS)
        logger.debug("Poll attempt %d/%d for token %s", attempt, MAX_POLL_ATTEMPTS, token)

        resp = requests.get(get_url, headers=headers, timeout=15)
        resp.raise_for_status()
        last_data = resp.json()

        status_id = (last_data.get("status") or {}).get("id", 0)
        if status_id not in (STATUS_IN_QUEUE, STATUS_PROCESSING):
            return last_data

    # Max attempts reached - return whatever we last received
    logger.warning(
        "Reached max poll attempts (%d) for token %s; returning last response.",
        MAX_POLL_ATTEMPTS,
        token,
    )
    return last_data


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def execute_code(source_code: str, language: str, stdin: str = "") -> dict:
    """
    Execute source code via Judge0 and return the result.

    Parameters
    ----------
    source_code : str
        The source code to compile/interpret and run.
    language : str
        One of "python", "cpp", "java", "javascript" (case-insensitive).
    stdin : str, optional
        Standard input to feed to the program.

    Returns
    -------
    dict with keys:
        stdout, stderr, compile_output, status, status_id, runtime, memory

    Raises
    ------
    ValueError
        If the language is not supported.
    requests.HTTPError
        If the Judge0 API returns a non-2xx response.
    """
    lang_key = language.strip().lower()
    if lang_key not in LANGUAGE_IDS:
        supported = ", ".join(LANGUAGE_IDS.keys())
        raise ValueError(
            f"Unsupported language '{language}'. Supported languages: {supported}"
        )

    language_id = LANGUAGE_IDS[lang_key]
    api_url: str = Config.JUDGE0_API_URL.rstrip("/")
    api_key = getattr(Config, "JUDGE0_API_KEY", None) or None

    headers = _build_headers(api_url, api_key)

    payload = {
        "source_code": _encode(source_code),
        "language_id": language_id,
        "stdin": _encode(stdin),
        "base64_encoded": True,
        "wait": True,
    }

    logger.debug(
        "Submitting code to Judge0: language=%s (id=%d), api_url=%s",
        lang_key,
        language_id,
        api_url,
    )

    # POST the submission with wait=true for a synchronous response when possible
    submit_url = f"{api_url}/submissions?base64_encoded=true&wait=true"
    response = requests.post(submit_url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    data: dict = response.json()

    # Some Judge0 deployments return a token even with wait=true when the queue
    # is busy. Handle polling for those cases.
    submission_token = data.get("token")
    status_obj = data.get("status") or {}
    status_id = status_obj.get("id", 0)

    if status_id in (STATUS_IN_QUEUE, STATUS_PROCESSING) and submission_token:
        logger.debug(
            "Submission %s is in queue/processing; starting poll loop.",
            submission_token,
        )
        data = _poll_until_done(api_url, submission_token, headers)

    result = _parse_response(data)
    logger.debug("Judge0 result status: %s", result["status"])
    return result


def get_languages() -> list:
    """
    Return the list of languages supported by this service with their Judge0 IDs.

    Returns
    -------
    list of dicts, each with keys:
        name  - human-readable language name
        key   - lowercase key used in execute_code()
        id    - Judge0 language ID integer
    """
    return [
        {"name": "Python 3", "key": "python", "id": LANGUAGE_IDS["python"]},
        {"name": "C++ (GCC)", "key": "cpp", "id": LANGUAGE_IDS["cpp"]},
        {"name": "Java (OpenJDK)", "key": "java", "id": LANGUAGE_IDS["java"]},
        {"name": "JavaScript (Node.js)", "key": "javascript", "id": LANGUAGE_IDS["javascript"]},
    ]
