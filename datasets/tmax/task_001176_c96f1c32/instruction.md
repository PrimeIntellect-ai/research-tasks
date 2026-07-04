You are a security log analyst investigating a recent anomalous event. A system administrator left a voice memo detailing an incident, but the exact server hostname they mentioned might have been mispronounced or corrupted by audio noise. You need to identify the exact server they meant by comparing the transcription against our legacy server inventory.

You have the following resources:
1. An audio file at `/app/incident_report.wav` containing the administrator's voice memo.
2. A legacy server inventory file at `/home/user/server_inventory.bin`. This file contains one hostname per line but is encoded in `UTF-16LE`.

Your task is to build a Python-based data processing pipeline and a query service that does the following:

1. **Audio Transcription**: Transcribe the audio file `/app/incident_report.wav` to text. You may install and use any Python package (like `SpeechRecognition` with Sphinx, or `openai-whisper` if you prefer). 
2. **Data Ingestion**: Read the `server_inventory.bin` file, properly handling its character encoding.
3. **Similarity Computation**: Implement a string similarity function (using Levenshtein distance) to compare any given string against all hostnames in the inventory.
4. **Service Deployment**: Bring up an HTTP REST API server (e.g., using Flask or FastAPI) listening exactly on `127.0.0.1:8000`.

The HTTP server must implement the following endpoints:
- `GET /api/transcript`
  Returns a JSON response with the exact transcribed text: `{"transcript": "..."}`
- `POST /api/match`
  Accepts a JSON payload like `{"query": "spoken server name"}`.
  Returns a JSON response with the closest matching hostname from the inventory and the Levenshtein distance: `{"closest_match": "server_hostname", "distance": integer_value}`

Ensure your server remains running in the foreground or background so it can be tested. Do not use any authentication on the server. Write and execute the code to stand up this service.