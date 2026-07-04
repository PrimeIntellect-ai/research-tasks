I am a researcher organizing field datasets, and I need your help extracting data from a set of compressed logs and a voice note, and then exposing this data via a local web service.

You will find the following in the environment:
1. A recursive directory structure under `/app/dataset/logs/` containing many compressed log files (e.g., `.log.gz`).
2. An audio recording of my field note at `/app/field_audio.wav`.

**Step 1: Log Parsing**
The log files contain multi-line event records. Each record looks exactly like this:
```
---BEGIN RECORD---
Timestamp: <ISO-8601-Date>
SensorID: <String>
Reading: <Float>
AnomalyFlag: <TRUE|FALSE>
---END RECORD---
```
You need to recursively search through all `.log.gz` files in the dataset, read the compressed streams without fully decompressing them to disk, and extract the `Timestamp` for every record where `AnomalyFlag: TRUE`. Sort these timestamps chronologically.

**Step 2: Audio Transcription**
Analyze and transcribe the audio file located at `/app/field_audio.wav`. You may install and use any Python libraries or CLI tools (like `whisper`, `SpeechRecognition`, `pocketsphinx`, etc.) available to transcribe the English speech in the WAV file. 

**Step 3: Web Server**
Write and start a Python HTTP server listening on `127.0.0.1:8080`. The server must have the following endpoints:
*   `GET /anomalies` : Returns a JSON array of strings containing the chronologically sorted anomaly timestamps.
*   `GET /transcript` : Returns a JSON object in the exact format: `{"transcript": "<transcribed_text_here>"}` (capitalization and punctuation don't strictly matter as long as the core words are correct, but try to be accurate).

Keep the server running in the background once it is ready so that my automated tools can query it.