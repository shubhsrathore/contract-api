import os
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import traceback

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Langflow API URL (update with your correct flow ID)
LANGFLOW_URL = "http://localhost:7860/api/v1/run/038a0403-3cc9-454e-8a51-433318cda497?stream=false"

# Directory to save uploaded files
UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process_contract/")
async def process_contract(file: UploadFile = File(...)):
    try:
        # Step 1: Save uploaded file to disk so Langflow can access it
        file_ext = os.path.splitext(file.filename)[-1]
        saved_filename = f"{uuid.uuid4().hex}{file_ext}"
        saved_path = os.path.join(UPLOAD_DIR, saved_filename)

        # Save the file to disk
        with open(saved_path, "wb") as f:
            f.write(await file.read())

        # Step 2: Prepare Langflow payload with the saved file path
        langflow_payload = {
            "output_type": "chat",
            "input_type": "text",
            "tweaks": {
                "Unstructured-FJRkv": {
                    "path": saved_path,
                    "api_key": "sSSLAoHwDvyDUygWXJsXeyxRDMNC5h",  # Ensure this API key is correct
                    "api_url": "https://api.unstructuredapp.io/general/v0/general",
                    "chunking_strategy": "basic",
                    "delete_server_file_after_processing": True,
                    "ignore_unspecified_files": False,
                    "ignore_unsupported_extensions": True,
                    "silent_errors": False,
                    "unstructured_args": "{}"
                },
                "Prompt-vSTeu": {
                    "Question": ""  # You can add a specific question here if needed
                }
            }
        }

        # Send the request to Langflow
        headers = {"Content-Type": "application/json"}
        response = requests.post(LANGFLOW_URL, headers=headers, json=langflow_payload)

        # Check if Langflow API responds successfully
        if response.status_code != 200:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Langflow API error", "langflow_response": response.text}
            )

        # Step 3: Parse the Langflow response (this depends on your Langflow output format)
        langflow_output = response.json()

        # Return the Langflow output as a response
        return JSONResponse(content={"status": "success", "data": langflow_output})

    except Exception as e:
        # Catch any errors and return the message
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
