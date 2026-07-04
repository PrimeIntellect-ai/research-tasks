You are tasked with recovering the configuration history for a legacy system and exposing it via a REST API. The configuration manager tracked changes by writing them into a custom compressed archive format, and the original API authentication key was lost, save for a screenshot of an old dashboard.

Your workflow consists of the following steps:

1. **Extract the API Key (Image Processing)**
   There is a screenshot of the legacy system dashboard located at `/app/legacy_dashboard.png`. Use OCR (e.g., `tesseract`, which is installed) to extract the text. The image contains a line that looks like `API_SALT: <secret_string>`. You must recover this `<secret_string>` exactly.

2. **Decompress the Configuration Archive (Custom Stream Processing)**
   The configuration history is stored in `/app/config_archive.lzc`. This file uses a custom "Log Zipped Chunks" (LZC) format. 
   - The file begins with a 4-byte magic signature: `LZC1` (ASCII).
   - Following the signature is a sequence of chunks.
   - Each chunk starts with a 4-byte big-endian unsigned integer representing the `compressed_size` of the chunk.
   - This is immediately followed by `compressed_size` bytes of zlib-compressed data.
   Write a Python script to decompress this file stream into raw text.

3. **Parse the Multi-line Logs**
   The decompressed text contains multi-line configuration change records. Each record has the following strict format:
   ```
   ===CONFIG_CHANGE===
   Time: <epoch_timestamp>
   User: <username>
   Module: <module_name>
   ---
   <diff_line_1>
   <diff_line_2>
   ...
   ===================
   ```
   Note: The diff lines can be any number of lines starting with `+` or `-`.

4. **Serve the Data via HTTP API**
   Create a Python HTTP server (e.g., using Flask, FastAPI, or `http.server`) that listens on `127.0.0.1:8000`.
   - The API must implement a `GET /config/<module_name>` endpoint.
   - It should return a JSON list of all configuration changes for the given `<module_name>`, ordered by `Time` ascending.
   - Each object in the JSON list should have the format:
     `{"time": 1696161600, "user": "sysadmin", "changes": ["+ ip_forwarding=1", "- ip_forwarding=0"]}`
   - **Authentication:** The API MUST require an `Authorization` header containing exactly the `<secret_string>` extracted from the dashboard image in Step 1. If the header is missing or incorrect, return a `403 Forbidden` status code. If the module is not found, return an empty list `[]` (with a 200 OK status).

Leave the API running in the background when you are finished. Ensure all your scripts are robust.