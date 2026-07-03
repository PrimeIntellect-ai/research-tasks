You are an ETL data engineer. We have a SQLite database located at `/app/data/analytics.db` containing a table called `events` (with columns `event_id`, `user_id`, `event_type`, `event_timestamp`, and `revenue`).

Additionally, there is an audio file at `/app/instructions.wav` left by the lead data scientist. The audio contains instructions on how to process this data and how to serve it. 

Your task is to:
1. Transcribe the audio file to understand the specific data processing and serving requirements. You may use Python libraries like `openai-whisper` or `SpeechRecognition` to transcribe the audio.
2. Connect to the SQLite database and extract the data using the logic specified in the audio. This will involve window functions, aggregation, and filtering.
3. Build a Python web service (e.g., using Flask or FastAPI) that exposes the processed results exactly as instructed in the audio.
4. Ensure the service is running in the background and listening on the specified port and endpoint.

The database and audio file are already present in the `/app/` directory. Please set up the pipeline and leave the API running.