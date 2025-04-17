import os
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LANGFLOW_URL = "http://localhost:7860/api/v1/run/038a0403-3cc9-454e-8a51-433318cda497?stream=false"
UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process_contract/")
async def process_contract(file: UploadFile = File(...)):
    try:
        # Step 1: Save uploaded file to disk so Langflow can access it
        file_ext = os.path.splitext(file.filename)[-1]
        saved_filename = f"{uuid.uuid4().hex}{file_ext}"
        saved_path = os.path.join(UPLOAD_DIR, saved_filename)

        with open(saved_path, "wb") as f:
            f.write(await file.read())

        # Step 2: Prepare Langflow payload with the saved file path
        langflow_payload = {
            "output_type": "chat",
            "input_type": "text",
            "tweaks": {
                "Unstructured-FJRkv": {
                    "path": saved_path
                },
                "Prompt-vSTeu": {
                    "Question": ""
                }
            }
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(LANGFLOW_URL, headers=headers, json=langflow_payload)

        if response.status_code != 200:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Langflow API error", "langflow_response": response.text}
            )

        langflow_output = response.json()
        return JSONResponse(content={"status": "success", "data": langflow_output})

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)})
