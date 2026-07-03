You are an automation specialist tasked with building a secure audio-to-text ETL workflow. We have a system that processes intercepted radio communications, but we need to ensure that any sensitive numerical identifiers (like spoken account numbers or security codes) are redacted before they enter our analytics database, while preserving benign numeric data (like quantities or times).

Your task has three phases:

**Phase 1: The Sanitize Function**
Write a Python module at `/home/user/pipeline/sanitizer.py` containing a function `sanitize_text(text: str) -> str`. This function must act as a quality gate. It should identify and redact sensitive numeric patterns (e.g., sequences of 9+ digits, standard credit card formats, SSNs) by replacing the digits with `[REDACTED]`. It must NOT alter standard text, dates, or small quantities.
To ensure your function is robust, it must pass a strict adversarial check against two datasets located at:
- `/app/corpus/clean/`: Contains 50 benign text snippets. Your function must return these exactly as they are.
- `/app/corpus/evil/`: Contains 50 snippets with embedded sensitive identifiers. Your function must successfully redact the identifiers in every snippet.

**Phase 2: Audio Extraction and Transcription**
We have an audio fixture located at `/app/input_stream.wav`.
1. Use an appropriate Python library (e.g., `SpeechRecognition`, `pydub`, or standard tools like `ffmpeg` combined with a local Whisper model if you choose to install one) to transcribe this audio file. 
2. The transcript must be broken down into chunks (sentences or 5-second segments).

**Phase 3: Transformation, Joining, and Rolling Stats**
You are provided with a metadata file at `/app/speaker_metadata.csv` containing columns `start_time`, `end_time`, and `speaker_id`.
Create a main ETL script at `/home/user/pipeline/etl.py` that does the following:
1. Takes the transcribed chunks and their timestamps.
2. Joins each chunk with the corresponding `speaker_id` from the CSV based on time overlap.
3. Streams the joined text through your `sanitize_text` function.
4. Computes a rolling statistic: the rolling average of redacted words over the last 3 processed chunks.
5. Emits pipeline monitoring logs to `/home/user/pipeline/etl.log` whenever a redaction occurs.

**Final Output**
The pipeline must output a final JSON file at `/home/user/pipeline/output.json` with the following schema:
```json
[
  {
    "timestamp": 0.0,
    "speaker_id": "ALPHA",
    "original_length": 45,
    "sanitized_text": "The subject reported the quantity as forty five.",
    "rolling_redaction_avg": 0.0
  },
  ...
]
```
Ensure your environment setup installs any necessary dependencies.