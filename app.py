from fastapi import FastAPI
import time
import uuid

from pipeline.intent import extract_intent
from pipeline.design import design_system
from pipeline.schema_gen import generate_schema
from pipeline.refine import refine
from pipeline.validate import validate_and_repair

from evaluation import track

# Create FastAPI app
app = FastAPI()


# Home route
@app.get("/")
def home():
    return {
        "message": "AI Compiler Running 🚀"
    }


# Generate endpoint
@app.post("/generate")
def generate_app(user_input: str):

    start_time = time.time()

    request_id = str(uuid.uuid4())[:8]

    try:

        # Step 1: Intent Extraction
        intent = extract_intent(user_input)

        if "error" in intent:
            return {
                "request_id": request_id,
                "stage": "intent",
                **intent
            }

        # Step 2: Design System
        design = design_system(intent)

        if "error" in design:
            return {
                "request_id": request_id,
                "stage": "design",
                **design
            }

        # Step 3: Generate Schema
        schema = generate_schema(design)

        if "error" in schema:
            return {
                "request_id": request_id,
                "stage": "schema",
                **schema
            }

        # Step 4: Refine Schema
        schema = refine(schema)

        # Step 5: Validate + Repair
        schema, errors = validate_and_repair(schema)

        # Step 6: Metrics
        stats = track(start_time, errors)

        return {
            "request_id": request_id,
            "intent": intent,
            "design": design,
            "final_schema": schema,
            "errors": errors,
            "metrics": stats
        }

    except Exception as e:

        return {
            "request_id": request_id,
            "error": "system_crash",
            "details": str(e)
        }