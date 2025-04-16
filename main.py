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


@app.post("/process_contract/")
async def process_contract(file: UploadFile = File(...)):
    # Step 1: Read the file
    content = await file.read()

    # Step 2: Simulated response (will be replaced with real Langflow connection later)
    result = [
        {"clause": "Payment due in 60 days", "topic": "payment terms", "risk_score": 3},
        {"clause": "Delivery within 8 weeks", "topic": "delivery", "risk_score": 4}
    ]

    return JSONResponse(content={"status": "success", "data": result})
