You are assisting a technical writer in organizing a vast, legacy documentation archive into a modernized web stack. The archive contains old text files in various character encodings, but unfortunately, it has also been polluted with corrupted and potentially malicious files.

Your task has two main phases: building an adversarial document sanitizer, and configuring the multi-service documentation viewer stack.

**Phase 1: Document Sanitizer**
Create a Python script at `/home/user/sanitizer.py`. It must accept two command-line arguments: `--input` (the directory to process) and `--output` (the directory where sanitized files will be written). 
The script must:
1. Read the configuration file at `/app/config/sanitizer_config.json`. This file contains a list of allowed input encodings (under the key `allowed_encodings`) and the target output encoding (under `target_encoding`).
2. Iterate through all files in the `--input` directory.
3. Attempt to read each file. A file is considered "clean" and should be processed IF AND ONLY IF:
   - It can be successfully decoded using at least one of the `allowed_encodings` (try them in the order listed).
   - It does NOT contain any null bytes (`\x00`).
   - It does NOT contain the substring `<script>` (case-insensitive).
4. For clean files, write them to the `--output` directory using the `target_encoding`.
5. Files that fail any of the conditions in step 3 are considered "evil" and must be completely skipped.
6. Generate a manifest file named `manifest.json` in the `--output` directory. It must have the following exact JSON structure:
   ```json
   {
     "files": [
       {
         "filename": "example.txt",
         "sha256": "<hex_sha256_of_converted_output_content>"
       }
     ]
   }
   ```

**Phase 2: Multi-Service Stack Integration**
We use a stack consisting of Nginx, a Flask backend (provided at `/app/server.py`), and Redis.
1. Write an Nginx configuration file at `/home/user/nginx.conf`. It must run in the foreground (`daemon off;`), listen on port `8080`, and configure two routes:
   - `GET /manifest.json`: Serve the `manifest.json` file directly from `/home/user/processed_docs/manifest.json`.
   - `GET /docs/<filename>`: Proxy the request to the Flask backend running on `http://127.0.0.1:5000/`.
2. Process the raw docs: Run your sanitizer to process the files in `/app/data/raw/` and output them to `/home/user/processed_docs/`.
3. Start Redis: `redis-server --daemonize yes`
4. Start the Flask backend: `DOC_DIR=/home/user/processed_docs python3 /app/server.py &`
5. Start Nginx: `nginx -c /home/user/nginx.conf &`

Ensure the entire system is running and correctly wired so that the Nginx proxy responds appropriately.