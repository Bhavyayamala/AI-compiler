import json
import re
from llm import call_llm

def extract_intent(user_input):
    prompt = f"""
    Extract structured intent from:
    {user_input}

    Return ONLY JSON with:
    app_type, features, roles
    """

    response = call_llm(prompt)

    if isinstance(response, dict):
        return response

    try:
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            return {"error": "no_json_found", "raw": response}

    except Exception as e:
        return {"error": "invalid_json", "details": str(e), "raw": response}