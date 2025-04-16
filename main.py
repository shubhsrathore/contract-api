from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Let WeWeb or any other frontend connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/process_contract")
async def process_contract(file: UploadFile = File(...)):
    # Simulate Langflow execution
    # Replace this block with Langflow pipeline execution logic
    contract_text = await file.read()

    # Simulated LLM result for now
    processed_data = [
        {"clause": "Payment due in 60 days", "topic": "payment terms", "risk_score": 3},
        {"clause": "Delivery in 8 weeks", "topic": "delivery", "risk_score": 4},
        {"clause": "1 year warranty", "topic": "warranty", "risk_score": 1}
    ]

    return {"data": processed_data}
