import json
import re
from llm import call_llm

def generate_schema(design):
    prompt = f"""
    You are building a real application system.

    Based on this design:
    {design}

    Generate STRICT JSON with:

    ui:
      pages: list of pages with components

    api:
      endpoints: list of endpoints with path, method

    db:
      tables: list of tables with fields

    auth:
      roles and permissions

    IMPORTANT:
    - UI, API, DB must be DIFFERENT
    - API must relate to DB
    - UI must use API
    - Return ONLY JSON
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