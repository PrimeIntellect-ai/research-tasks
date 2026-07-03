You are assisting a technical writer in securing a fully automated, multi-service documentation ingestion pipeline. Community contributors submit documentation drafts as ZIP archives, which are processed, sanitized, and eventually stored.

Currently, the pipeline in `/home/user/app/` is broken and vulnerable to malicious submissions. The pipeline consists of:
1. An Nginx reverse proxy listening on port 8080.
2. A Flask application (`doc-receiver`) running on port 5000.
3. A Redis server for job queuing.

Your task is to fix the pipeline and build a robust sanitizer script.

**Step 1: Fix the Pipeline Glue**
Nginx is supposed to proxy POST requests from `http://127.0.0.1:8080/upload` to the Flask app. However, Nginx is currently misconfigured and the end-to-end flow fails. You must edit `/home/user/app/nginx.conf` and any Flask configuration in `/home/user/app/receiver.py` to ensure submissions reach the Flask app successfully and are queued in Redis. 

**Step 2: Develop the Sanitizer**
Write a Python CLI tool at `/home/user/sanitizer.py` that will be used to process the uploaded archives. 
Usage must be: `python3 /home/user/sanitizer.py <input_zip_path> <output_dir>`

The sanitizer must implement the following logic:
- **Nested Archive Handling & Integrity Validation:** It must extract the provided ZIP file. If there are any ZIP files *inside* the extracted contents, it must extract those as well (up to 2 levels deep). During extraction, it must verify the integrity of the archives. If an archive is corrupted (e.g., bad CRC), or if any single file inside the archive is larger than 1MB when uncompressed (to prevent zip bombs), the script must immediately abort and exit with a non-zero exit code.
- **Content Sanitization:** For all extracted `.md` (Markdown) and `.txt` files, you must scan them and remove any line containing the exact string `<script>`. Write the sanitized files to `<output_dir>`.
- **Format Conversion:** Any `.txt` files found should be renamed to `.md` in the output directory.

If the file is completely safe and successfully sanitized/extracted, the script should exit with code 0. If it detects corruption, a zip bomb, or is unable to process it safely, it must exit with code 1.

Ensure your `sanitizer.py` script is robust against unexpected edge cases, as it will be rigorously tested against an adversarial test suite.