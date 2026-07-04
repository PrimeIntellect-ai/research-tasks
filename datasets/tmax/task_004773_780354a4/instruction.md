You are an artifact manager building a secure binary repository ingestion service. 

We receive custom binary archives from build pipelines, but we've recently discovered that some of these archives are malicious and attempt "Zip Slip" attacks (path traversal). 

Your task is to write a C-based HTTP server that receives these archives, verifies authorization, securely parses them, and extracts the safe files.

**Step 1: Authorization Directive**
Listen to the audio file located at `/app/directive.wav`. It contains a short spoken phrase. The exact spoken phrase (all lowercase, no punctuation) must be used as the expected bearer token.

**Step 2: Configuration**
Parse the configuration file at `/home/user/server.conf`. It contains key-value pairs (e.g., `port=8080`, `extract_dir=/home/user/artifacts`). Your server must listen on the specified port on `127.0.0.1` and extract files into the specified directory. You must create the `extract_dir` if it doesn't exist.

**Step 3: The HTTP Server**
Write a C program (`/home/user/artifact_server.c`) and compile it. The server must:
1. Listen for `POST /upload` requests.
2. Check for the `Authorization: Bearer <transcribed_phrase>` header. If missing or incorrect, return `401 Unauthorized`.
3. Read the request body as a custom binary archive (the "ARTF" format).

**Step 4: The ARTF Format & Secure Extraction**
The ARTF binary format is structured as follows:
- Magic bytes: `ARTF` (4 bytes)
- Number of files: 16-bit unsigned integer, little-endian (2 bytes)
- Followed by the file entries. Each entry:
  - Filename length: 16-bit unsigned integer, little-endian (2 bytes)
  - Filename: ASCII string of the specified length (NOT null-terminated)
  - File size: 32-bit unsigned integer, little-endian (4 bytes)
  - File data: raw bytes of the specified size

*Security Requirement (Zip Slip Mitigation):* 
Iterate through the files. If ANY filename in the archive is an absolute path (starts with `/`) or contains path traversal sequences (`../`), you must abort the entire process, extract NO files from the archive, and immediately return a `400 Bad Request` HTTP response.
If the archive is completely safe, extract all files into the `extract_dir`, preserving their provided relative paths (you may assume subdirectories do not need to be created for safe files; filenames will just be standard names like `app.bin`), and return `200 OK`.

Compile and run your server in the background. Leave it running so our verification suite can test it.