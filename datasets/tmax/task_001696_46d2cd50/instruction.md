You are a backup administrator recovering from a partial storage array failure. You need to identify intact backup chunks, extract their metadata, and expose a secure API endpoint so the central backup orchestrator can retrieve the manifest.

Your task consists of the following steps:

1. **Extract the API Token**:
   The backup system generated a physical label containing the secure API token required for the orchestrator to communicate with your recovery server. A scanned image of this label is located at `/app/auth_label.png`. You must extract the text from this image to use as the Bearer token.

2. **Identify Valid Backup Chunks**:
   The directory `/app/archive_data/` contains many `.dat` files in subdirectories. Due to the array failure, some files are corrupted. A valid backup chunk ALWAYS starts with the 4-byte magic sequence: `42 41 4B 01` (in hex). You must recursively traverse the directory and identify all valid `.dat` files.

3. **Parse Metadata**:
   There is a file `/app/archive_data/index.csv` with the headers: `filename,owner,timestamp`. 
   For every valid `.dat` file you found in step 2, look up its `filename` in the CSV to find the `owner` and `timestamp`.
   Construct a JSON file named `/home/user/manifest.json` containing an array of objects for the valid files. The format must exactly match:
   `[{"filename": "chunk_name.dat", "owner": "...", "timestamp": "..."}, ...]`
   Order the JSON array alphabetically by `filename`.

4. **Serve the Manifest**:
   Write a Bash-based HTTP server using `socat` (or `nc`) that listens on `0.0.0.0:8080`.
   - The server must respond to `GET /api/manifest HTTP/1.1`
   - It must require the HTTP header: `Authorization: Bearer <TOKEN>` (where `<TOKEN>` is the text you extracted from the image).
   - If the token is correct, return a `200 OK` HTTP response with `Content-Type: application/json` and the contents of `/home/user/manifest.json`.
   - If the token is missing or incorrect, return `401 Unauthorized`.
   - Leave this server running in the background.

Use Bash scripts for the implementation. You may use standard tools like `jq`, `grep`, `hexdump`, `awk`, `socat`, and `tesseract` which are available on the system.