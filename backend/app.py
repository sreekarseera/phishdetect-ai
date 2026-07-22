import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

model = joblib.load("model/model.joblib")

class Message(BaseModel):
    text: str

@app.post("/classify/")
def classify(msg: Message):
    label = int(model.predict([msg.text])[0])
    score = float(model.predict_proba([msg.text])[0][label])
    explanation = "Potential scam." if label else "Message looks safe."
    return {"label": f"LABEL_{label}", "score": score, "explanation": explanation}