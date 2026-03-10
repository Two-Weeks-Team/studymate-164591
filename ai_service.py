import os
import json
import re
from typing import Any, List, Dict
import httpx

DO_INFERENCE_URL = "https://inference.do-ai.run/v1/chat/completions"
DEFAULT_MODEL = os.getenv("DO_INFERENCE_MODEL", "openai-gpt-oss-120b")
AUTH_KEY = os.getenv("DIGITALOCEAN_INFERENCE_KEY")

# ---------------------------------------------------------------------------
# Helper to pull JSON out of LLM "markdown" wrappers
# ---------------------------------------------------------------------------
def _extract_json(text: str) -> str:
    m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()

# ---------------------------------------------------------------------------
# Core async inference call – single place for timeout, auth, error handling
# ---------------------------------------------------------------------------
def _coerce_unstructured_payload(raw_text: str) -> Dict[str, Any]:
    compact = raw_text.strip()
    tags = [part.strip(" -•\t") for part in re.split(r",|\\n", compact) if part.strip(" -•\t")]
    return {
        "note": "Model returned plain text instead of JSON",
        "raw": compact,
        "text": compact,
        "summary": compact,
        "tags": tags[:6],
    }


async def _call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Any:
    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "max_completion_tokens": max_tokens,
    }
    headers = {"Authorization": f"Bearer {AUTH_KEY}"} if AUTH_KEY else {}
    timeout = httpx.Timeout(90.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            resp = await client.post(DO_INFERENCE_URL, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            # Expected shape: {"choices": [{"message": {"content": "..."}}]}
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            json_str = _extract_json(content)
            return json.loads(json_str)
        except Exception as e:
            # Log could be added here; for now, return a fallback structure
            return {"note": "AI service temporarily unavailable: " + str(e)}

# ---------------------------------------------------------------------------
# Public helpers used by route handlers – keep them thin wrappers
# ---------------------------------------------------------------------------
async def generate_study_plan(syllabus: str, start_date: str) -> Dict[str, Any]:
    system_prompt = (
        "You are a study‑plan generator. Given a syllabus and a start date, produce a JSON object "
        "with keys: 'plan_id' (string), 'topics' (list of objects with 'topic_id', 'name', "
        "'study_days' (list of ISO dates), and 'completion_status' (bool), and 'end_date' (ISO date)."
    )
    user_prompt = f"Syllabus:\n{syllabus}\nStart Date: {start_date}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    return await _call_inference(messages, max_tokens=512)

async def generate_revision_cards(material: str) -> List[Dict[str, Any]]:
    system_prompt = (
        "You are an expert at creating concise revision flashcards. Return a JSON array where each "
        "element has 'front' (question or term) and 'back' (answer or explanation)."
    )
    user_prompt = f"Material:\n{material}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    result = await _call_inference(messages, max_tokens=512)
    # Ensure we always return a list
    if isinstance(result, list):
        return result
    return []
