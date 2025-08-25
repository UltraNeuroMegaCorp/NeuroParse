import asyncio

from fastapi import FastAPI, File, UploadFile
import whisper
import os

app = FastAPI()

VOICES_DIR = "voice_messages"

os.makedirs(VOICES_DIR, exist_ok=True)

model = whisper.load_model("medium")

print("model loaded")


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    file_path = os.path.join(VOICES_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: model.transcribe(file_path, fp16=False))
        text = result["text"].strip()
        os.remove(file_path)
    return {"text": text}

@app.get("/health")
async def health():
    return {"status": "ok"}

