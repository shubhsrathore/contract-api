from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import traceback

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (WeWeb frontend etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process_contract/")
async def process_contract(file: UploadFile = File(...)):
    try:
        # Step 1: Read the uploaded file
        content = await file.read()

        # Step 2: Simulated Langflow response
        result = [
            {"clause": "Payment due in 60 days", "topic": "payment terms", "risk_score": 3},
            {"clause": "Delivery within 8 weeks", "topic": "delivery", "risk_score": 4}
        ]

        return JSONResponse(content={"status": "success", "data": result})
    
    except Exception as e:
        traceback.print_exc()  # Log to terminal
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
