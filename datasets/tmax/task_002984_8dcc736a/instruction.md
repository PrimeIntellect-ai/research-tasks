You are an AI assistant helping a technical writer implement a robust, high-efficiency backup system for a highly active documentation generation pipeline. 

The technical writer has a multi-service setup located in `/app/`:
1. **`doc_writer.py`**: A continuously running process that simulates an active team of writers and build systems. It constantly creates, updates, and appends to files in `/app/docs/`. It uses strict OS-level file locking (`fcntl.LOCK_EX`) when writing to prevent data corruption.
2. **`doc_metastore`**: A Redis instance running on `localhost:6379` (db 0). It tracks the `last_modified` timestamp and `original_encoding` of every text file.
3. **`doc_server.py`**: A local Flask application on port 5000 that serves the documentation.

**Your task:**
Write a Python script at `/home/user/archiver.py` that creates an incremental, highly compressed backup of `/app/docs/`. Save your final backup archive at `/home/user/backup.tar.xz`.

Your archiver must meet the following requirements:
1. **Concurrency & File Locking:** You must safely read files from `/app/docs/` without crashing or reading corrupted data if `doc_writer.py` is currently writing to them. If a file is exclusively locked, your script must wait or retry until it can acquire a shared lock (`fcntl.LOCK_SH`).
2. **Incremental Backup:** Only archive files that have been modified since the timestamp stored in `/home/user/last_run.txt` (if the file doesn't exist, assume timestamp 0). Update this file with the current Unix timestamp after a successful backup.
3. **Encoding Conversion:** The `doc_writer.py` creates text files (`.txt`, `.md`) in various legacy encodings (like `ISO-8859-1`, `Shift-JIS`). You must query Redis for the key `encoding:<filename>` to get the original encoding, convert the file's content to `UTF-8`, and store the UTF-8 version in your archive.
4. **Binary Header Extraction:** The directory also contains binary files (`.media`). Do not archive the full binary files (they are too large). Instead, extract the custom binary header (the first 32 bytes) from each modified `.media` file and store them as a mapping of `{"filename": "hex-encoded-header"}` in a single `media_headers.json` file at the root of your archive.
5. **High Efficiency:** You must use Python's `tarfile` with LZMA compression (`.tar.xz`) to maximize the compression ratio.

**Workflow:**
1. Start the documentation pipeline by running `/app/start_services.sh`. Let it run in the background.
2. Wait a few seconds for it to generate initial data.
3. Run your `/home/user/archiver.py` script.
4. The automated test will stop the services and evaluate your `/home/user/backup.tar.xz`.

**Evaluation Metric:**
Your output will be evaluated by an automated verifier that computes a `Storage Efficiency Score`. 
The formula is: `Efficiency Score = (Total size of correctly converted UTF-8 text files + size of correctly extracted media headers) / (File size of backup.tar.xz)`.
Because LZMA compresses text very well, and because you are stripping out heavy binary data in favor of just headers, your `Efficiency Score` must be **>= 4.5**.

Ensure your Python code is robust and handles the required logic precisely.