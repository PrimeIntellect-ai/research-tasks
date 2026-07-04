You are a backup administrator investigating a recent security incident. The attacker left behind a surveillance video `/app/surveillance.mp4` and a proprietary backup archive `/app/evidence.bkp`.

Your task is to build a C++ HTTP service that securely extracts these custom backup archives while preventing path traversal (Zip Slip) attacks, which the attacker previously exploited.

### Step 1: Recover the Archive Key
The attacker inadvertently recorded their screen. At exactly 00:00:03 in `/app/surveillance.mp4`, there is an overlay text containing the archive key in the format `KEY: <8-character-string>`.
Extract this frame (e.g., using `ffmpeg`) and use OCR (`tesseract-ocr` is recommended) to read the 8-character key. You will need this key to authorize extractions.

### Step 2: Build the Extraction Service
Write a C++ program that runs an HTTP server listening on `0.0.0.0:8000`. You may use single-header libraries like `httplib.h` (you can download it using `wget https://raw.githubusercontent.com/yhirose/cpp-httplib/master/httplib.h`) and `nlohmann/json` (available via `apt-get install nlohmann-json3-dev` or by downloading `json.hpp`).

**Endpoint:** `POST /restore`
**Request Content-Type:** `application/json`
**Request Body:** `{"archive": "<absolute_path_to_bkp>", "target": "<absolute_path_to_extract_directory>"}`

**The BKP1 File Format:**
The custom archive is a binary file with the following structure:
1.  **Magic Bytes:** `BKP1` (4 bytes, ASCII)
2.  **Encryption Key:** 8 bytes (ASCII). This MUST exactly match the key you recovered from the video. If it does not match, the server must return HTTP 403 Forbidden with body `{"error": "invalid key"}`.
3.  **File Entries (repeating until EOF):**
    *   **Path Length:** 2 bytes (unsigned 16-bit int, little-endian)
    *   **File Path:** *N* bytes (ASCII string)
    *   **File Size:** 4 bytes (unsigned 32-bit int, little-endian)
    *   **File Data:** *M* bytes (Raw binary data)

**Extraction Rules:**
1.  **Zip Slip Protection:** If a file path inside the archive starts with `/` or contains the substring `../`, it is considered malicious. Your parser MUST skip extracting this file and proceed to the next entry in the archive.
2.  **Atomic Writes:** To prevent partial extracts during crashes, every valid file must first be written to `<target_dir>/<file_path>.tmp`. Once fully written and flushed, it must be atomically renamed to `<target_dir>/<file_path>`. Make sure to create any necessary parent directories inside the target directory.
3.  **Response:** On successful processing of the entire archive, return HTTP 200 OK with a JSON body: `{"extracted": <count_of_valid_files>, "skipped": <count_of_malicious_files>}`.

### Execution
Compile your server (ensure you use `-std=c++17 -lpthread`), run it in the background, and leave it running. Do not exit. The automated verification system will send requests to `http://127.0.0.1:8000/restore` with a test archive to verify your zip slip protection, atomic write logic, and key validation.