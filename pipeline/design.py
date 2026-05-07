import json
import re
from llm import call_llm

def design_system(intent):
    prompt = f"""
    Convert this intent into system design:
    {intent}

    Return ONLY JSON with:
    entities, roles, flows
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