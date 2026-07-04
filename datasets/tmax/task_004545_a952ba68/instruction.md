You are acting as a storage administrator managing a legacy disk space consolidation project.

We have a nested archive file located at `/app/legacy_dump.tar.gz`. Additionally, there is a recovered audio file at `/app/secret_voicemail.wav`.

Your task requires you to perform the following steps:

1. **Nested Archive Extraction**:
   Extract `/app/legacy_dump.tar.gz` completely into `/app/unpacked/`. This archive contains nested archives (zips inside tars, etc.). You must recursively extract all of them until only the raw data files (`.txt`, `.dat`, `.wav`, etc.) remain in the directory tree under `/app/unpacked/`. Remove the intermediate archive files to save space.

2. **Bulk Renaming & Link Management**:
   Inside `/app/unpacked/`, recursively bulk rename all files so that their extensions are strictly lowercase (e.g., `.TXT` becomes `.txt`). 
   Create a single flat directory `/app/audio_links/` and create symbolic links inside it to all `.wav` files found anywhere within `/app/unpacked/`.

3. **Transcription**:
   Analyze the audio file `/app/secret_voicemail.wav`. It contains a short, spoken passphrase. You will need to transcribe this passphrase. You may install any tools you need to accomplish this.

4. **Service Implementation (Rust)**:
   Write a Rust application in `/app/storage_service/` that exposes an HTTP REST API. The service must listen on `127.0.0.1:8080`.
   - **Endpoint 1**: `GET /stats`
     Must return a JSON response with the total number of files in `/app/unpacked/` and the total number of symbolic links in `/app/audio_links/`:
     `{"files_count": <int>, "audio_links_count": <int>}`
   - **Endpoint 2**: `POST /unlock`
     Must accept a JSON payload: `{"passphrase": "<transcribed_text>"}`.
     If the transcribed text matches the spoken passphrase from `/app/secret_voicemail.wav` (ignoring case and punctuation), it should return HTTP 200 OK with body `{"status": "unlocked"}`. Otherwise, return HTTP 403 Forbidden.

Ensure the Rust server is compiled and running in the background before you finish. The automated verifier will issue HTTP requests to your service on `127.0.0.1:8080` to evaluate your work.