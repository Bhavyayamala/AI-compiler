def refine(schema):
    if "api" not in schema or "db" not in schema:
        schema["refined"] = False
    else:
        schema["refined"] = True

    return schema