We are trying to organize an old repository's legacy project files, but the only record we have of the older directory structures is a screencast video of a terminal archive. 

A video file is located at `/app/archive_scroll.mp4`. This video displays several project directories, each suffixed with a semantic version (e.g., `legacy-v1.0.2`, `legacy-v0.9.4-alpha`). 

Your task is to:
1. Extract the text from the video frames using tools of your choice (e.g., `ffmpeg` and `tesseract` are available on the system) to identify all the unique semantic versions shown in the video. Since video frame extraction and OCR can be slow, you should try to process frames concurrently.
2. Filter the extracted text to isolate valid semantic versions (the versions will start with 'v', like `v1.2.3`).
3. Organize the files logically by creating a text file at `/home/user/project_files/extracted_versions.txt` containing all unique, valid semantic versions found in the video. The list must be sorted in ascending semantic version order, one version per line.
4. Build and start a REST API (using any programming language you prefer) that serves this extracted version data. The API must listen on `127.0.0.1:8080` and remain running in the background.

The REST API must implement the following endpoints:
- `GET /api/versions/latest`: Returns a JSON object with the highest semantic version. 
  Format: `{"latest": "vX.Y.Z"}`
- `GET /api/versions/newer_than?v=<version>`: Compares the extracted versions against the query parameter (which will lack the 'v' prefix, e.g., `1.1.0`) and returns a JSON array of all versions strictly greater than the query parameter, sorted in ascending order.
  Format: `{"versions": ["vA.B.C", "vX.Y.Z"]}`

Start your REST API server in the background so that automated tests can verify its behavior.