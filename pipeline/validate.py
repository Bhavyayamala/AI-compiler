def validate_and_repair(schema):
    errors = []

    # -----------------------------
    # Extract data safely
    # -----------------------------
    db_tables = schema.get("db", {}).get("tables", [])
    api_endpoints = schema.get("api", {}).get("endpoints", [])
    ui_pages = schema.get("ui", {}).get("pages", [])

    table_names = [t["name"] for t in db_tables]
    api_paths = [e["path"] for e in api_endpoints]

    # -----------------------------
    # 🔍 VALIDATION
    # -----------------------------

    # API ↔ DB check
    for path in api_paths:
        if "contact" in path and "contacts" not in table_names:
            errors.append("Missing DB table: contacts")

        if "user" in path and "users" not in table_names:
            errors.append("Missing DB table: users")

    # UI ↔ API check
    for page in ui_pages:
        for comp in page.get("components", []):
            name = comp.get("name", "").lower()

            if "contact" in name and not any("contacts" in p for p in api_paths):
                errors.append("UI needs contacts API")

            if "login" in name and not any("login" in p for p in api_paths):
                errors.append("UI needs login API")

    # Duplicate API endpoints
    seen = set()
    for ep in api_endpoints:
        key = (ep["path"], ep["method"])
        if key in seen:
            errors.append(f"Duplicate API endpoint: {key}")
        seen.add(key)

    # -----------------------------
    # 🔧 REPAIR (targeted fixes)
    # -----------------------------

    # Fix DB tables
    if "contacts" not in table_names:
        db_tables.append({
            "name": "contacts",
            "fields": [
                {"name": "id", "type": "int"},
                {"name": "name", "type": "varchar"},
                {"name": "email", "type": "varchar"}
            ]
        })

    if "users" not in table_names:
        db_tables.append({
            "name": "users",
            "fields": [
                {"name": "id", "type": "int"},
                {"name": "username", "type": "varchar"},
                {"name": "password", "type": "varchar"}
            ]
        })

    schema["db"]["tables"] = db_tables

    # Remove duplicate APIs
    unique = []
    seen = set()
    for ep in api_endpoints:
        key = (ep["path"], ep["method"])
        if key not in seen:
            unique.append(ep)
            seen.add(key)

    schema["api"]["endpoints"] = unique

    # -----------------------------
    # Final Output
    # -----------------------------
    return schema, errors