from flask import Flask, request, jsonify
from pydub import AudioSegment
import whisper
import os
import math
import uuid

app = Flask(__name__)
API_KEY = "nzrdeniaue"

# Load Whisper model once
model = whisper.load_model("base")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    # API Key check
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    if "file" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["file"]
    file_ext = audio_file.filename.rsplit(".", 1)[-1].lower()
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join("/mnt/data", filename)
    audio_file.save(file_path)

    # Split into 5-minute chunks
    audio = AudioSegment.from_file(file_path)
    chunk_duration_ms = 5 * 60 * 1000
    total_chunks = math.ceil(len(audio) / chunk_duration_ms)
    transcript = ""

    for i in range(total_chunks):
        start_ms = i * chunk_duration_ms
        end_ms = min((i + 1) * chunk_duration_ms, len(audio))
        chunk = audio[start_ms:end_ms]
        chunk_path = f"/mnt/data/chunk_{uuid.uuid4()}.wav"
        chunk.export(chunk_path, format="wav")

        result = model.transcribe(chunk_path)
        transcript += f"\n--- Transcript for chunk {i + 1} ---\n{result['text']}"

        os.remove(chunk_path)  # Clean up

    os.remove(file_path)

    return jsonify({"transcript": transcript.strip()}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
