from flask import Flask, render_template, request, jsonify
from fastapi.middleware.wsgi import WSGIMiddleware
from typing import Annotated, Optional, Dict, Any
from fastapi import FastAPI, File, UploadFile
from npmai import Ollama
import pytesseract, cv2
import numpy as np
import os

flask_app = Flask(__name__, template_folder="templates", static_folder="static")

# Initialize LLM
llm = Ollama(
    model="llama3.2",
    temperature=0.8
)

@flask_app.route("/")
def index():
    return render_template("index.html")

# Endpoint to handle AI chat
@flask_app.route("/askAI", methods=["POST"])
def NPMai_ask():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt.strip():
        return jsonify({"response": "❗ Please provide a question."})

    try:
        result = llm.invoke(prompt)
        response = str(result)
    except Exception as e:
        response = f"❌ Error: {str(e)}"

    return jsonify({"response": response})

app=FastAPI()

app.mount("/flask",WSGIMiddleware(flask_app))

#OCR Handling
@app.post("/ocr")
async def create_upload_file(file: UploadFile):
    path = await file.read()
    nparr=np.frombuffer(path,np.uint8)
    img=cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text




