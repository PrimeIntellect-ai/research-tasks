You are an AI assistant helping a machine learning researcher automate their dataset ingestion pipeline. The researcher is working with voice recordings and needs a robust background service to organize incoming files automatically.

Your objective is to build and deploy a Python-based background service that performs file watching, audio transcription, hard-linking, and serves a status API.

Here are the detailed requirements:

1. Environment Setup:
   - Create a directory structure for the dataset: `/home/user/dataset/dropzone` and `/home/user/dataset/organized`.
   - Install any necessary Python packages (e.g., `watchdog`, `flask` or `fastapi`, `openai-whisper`, `uvicorn`, etc.). Note: Use the "tiny" whisper model to ensure it runs quickly.

2. File Watching & Organization Logic:
   - Write a Python script that recursively monitors the `/home/user/dataset/dropzone/` directory for any new `.wav` files.
   - When a new `.wav` file is created or moved into the dropzone (or its subdirectories), the script must transcribe the audio using Whisper.
   - The script must extract the transcribed text, strip any leading/trailing whitespace, and convert it to lowercase.
   - It must then create a subdirectory inside `/home/user/dataset/organized/` named exactly after the transcribed text.
   - Finally, it must create a **hard link** of the original `.wav` file into this new category directory, keeping the original filename. (e.g., `/home/user/dataset/organized/<transcription>/<filename>.wav`).

3. Status API:
   - The same Python application must run an HTTP server on `127.0.0.1:8000`.
   - It must expose a `GET /inventory` endpoint.
   - This endpoint must return a JSON object where the keys are the category names (the transcribed text) and the values are lists of absolute paths to the hard-linked files in that category. For example: `{"hello world": ["/home/user/dataset/organized/hello world/sample.wav"]}`.

4. Execution & Integration:
   - Start your Python background service.
   - There is a sample audio file provided at `/app/audio_sample.wav`.
   - Copy `/app/audio_sample.wav` into `/home/user/dataset/dropzone/test_folder/` to trigger the file watcher.
   - Wait for the file to be processed, transcribed, and hard-linked.
   - Ensure the API is responsive and reflects the newly organized file. Leave the service running in the background so it can be verified.