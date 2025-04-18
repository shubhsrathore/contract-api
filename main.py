import os, uuid, traceback
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True)

LANGFLOW_URL = "https://d03c-2402-e280-3e3f-391-71ac-e1ee-3701-e96.ngrok-free.app/api/v1/run/<your-flow-id>?stream=false"
UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process_contract/")
async def process_contract(file: UploadFile = File(...)):
    try:
        # save to disk
        ext = os.path.splitext(file.filename)[1]
        saved_name = f"{uuid.uuid4().hex}{ext}"
        saved_path = os.path.abspath(os.path.join(UPLOAD_DIR, saved_name))
        with open(saved_path, "wb") as out:
            out.write(await file.read())

        # prepare payload — make sure "Unstructured-XXX" matches your node ID!
        langflow_payload = {
            "output_type": "chat",
            "input_type": "text",
            "tweaks": {
                "Unstructured-FJRkv": {   # ←– REPLACE with your actual Node ID
                    "path": saved_path,
                    # any other fields your UnstructuredIO node needs…
                },
                "Prompt-vSTeu": {
                    "Question": ""
                }
            }
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(LANGFLOW_URL, headers=headers, json=langflow_payload)

        # debug logging
        print("↘ Langflow status:", response.status_code)
        print("↘ Langflow raw response:", repr(response.text))

        # handle non‑200
        if response.status_code != 200 or not response.text:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Langflow error", "details": response.text}
            )

        # parse JSON safely
        try:
            data = response.json()
        except ValueError:
            return JSONResponse(status_code=500, content={"status":"error","message":"Invalid JSON from Langflow","raw":response.text})

        return JSONResponse(content={"status": "success", "data": data})

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
