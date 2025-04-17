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

# Langflow API URL
LANGFLOW_URL = "http://localhost:7860/predict"  # or Render/other URL

@app.post("/process_contract/")
async def process_contract(file: UploadFile = File(...)):
    try:
        # Step 1: Read uploaded file content
        content = await file.read()
        contract_text = content.decode("utf-8", errors="ignore")

        # Step 2: Send text to Langflow chain
        langflow_payload = {
            "inputs": {
                "input": contract_text
            }
        }

        response = requests.post(LANGFLOW_URL, json=langflow_payload)

        if response.status_code != 200:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Langflow API error", "langflow_response": response.text}
            )

        langflow_output = response.json()

        # Step 3: Extract and optionally parse the result
        raw_output = langflow_output.get("output", "")

        # Step 4: (Optional) Parse output if it's structured as text
        # You can keep this as raw text or parse like before
        parsed = []
        blocks = raw_output.strip().split("\n\n")
        for block in blocks:
            lines = block.strip().split("\n")
            entry = {}
            for line in lines:
                if "Clause:" in line:
                    entry["clause"] = line.replace("Clause:", "").strip()
                elif "Topic:" in line:
                    entry["topic"] = line.replace("Topic:", "").strip()
                elif "Risk Score:" in line:
                    entry["risk_score"] = int(line.replace("Risk Score:", "").strip())
            if entry:
                parsed.append(entry)

        return JSONResponse(content={"status": "success", "data": parsed})

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
