from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated DB
with open("appeals.json") as f:
    appeals_db = json.load(f)

@app.get("/appeals/{user_id}")
def get_user_appeal(user_id: str):
    return appeals_db.get(user_id, {"status": "not found"})

@app.post("/appeals/{user_id}")
def submit_appeal(user_id: str, data: Dict):
    appeals_db[user_id] = data
    with open("appeals.json", "w") as f:
        json.dump(appeals_db, f, indent=2)
    return {"message": "Appeal submitted"}

@app.get("/ai_feedback/{user_id}")
def get_ai_feedback(user_id: str):
    # Simulated AI logic (with emotional sensitivity)
    data = appeals_db.get(user_id)
    if not data:
        return {"explanation": "No appeal found."}

    user_input = data.get("flag_reason", "").lower()
    if "no idea" in user_input or "don't know" in user_input or user_input.strip() == "":
        reason = "no clear reason was given"
        review_summary = (
            "We noticed your account was flagged without a clear explanation. "
            "This might be due to automated pattern detection or misclassification."
        )
    else:
        reason = user_input
        review_summary = f"Based on recent behavior, your account was flagged for: {reason}."

    return {
        "review_summary": review_summary,
        "human_touch": "It's okay to feel confused. You're not alone. "
                        "Our reviewers will look deeper into your case with care."
    }