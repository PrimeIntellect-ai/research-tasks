You are acting as a backup administrator managing an automated log archiving pipeline. We have a multi-service logging infrastructure consisting of a Flask ingestion API, a Redis message broker, and a Python archiving worker. Currently, the pipeline is misconfigured, and the archiving worker lacks the necessary sanitization logic to handle corrupted or malicious backup chunks.

Your objective is to fix the pipeline configuration, implement a strict binary format parser and sanitizer, and ensure the end-to-end archiving process works flawlessly.

### System Overview
The system is located in `/home/user/archiver/` and consists of:
1. **Flask API** (`/home/user/archiver/api.py`): Receives binary backup chunks via POST requests on port 8080.
2. **Redis**: Runs on a custom Unix socket at `/home/user/archiver/redis.sock`.
3. **Archiving Worker** (`/home/user/archiver/worker.py`): Pulls chunks from the Redis queue `backup_queue` and writes them to disk.

### Task Requirements

**Part 1: Service Configuration (Multi-Service Compose)**
- Modify `/home/user/archiver/api.py` to connect to Redis using the Unix socket `/home/user/archiver/redis.sock` instead of the default TCP port.
- Modify `/home/user/archiver/worker.py` to also connect to the same Redis Unix socket.
- Start Redis, the Flask API, and the Archiving Worker. (Configuration files like `redis.conf` are provided in the directory).

**Part 2: Binary Format Parsing & Sanitization**
The backup chunks are custom binary files with the following structure:
- **Magic Bytes (4 bytes):** `BKP1`
- **Header Length (4 bytes, unsigned integer, little-endian):** Specifies the length of the JSON header.
- **JSON Header (variable length):** Contains metadata, e.g., `{"timestamp": 1690000000, "source": "db_server", "checksum": "..."}`.
- **Payload (variable length):** The actual backup data.

You must implement a filtering function `sanitize_chunk(filepath)` in `/home/user/archiver/sanitizer.py`. The function must take a file path, parse the binary file, and return `True` if it is valid and clean, or `False` if it violates any of the following rules:
- **Rule 1:** The file must start with the exact magic bytes `BKP1`.
- **Rule 2:** The Header Length must not exceed 1024 bytes.
- **Rule 3:** The JSON Header must be valid, parsable JSON.
- **Rule 4:** The JSON Header must contain a `source` key. If the `source` is `"unknown"` or `"test"`, it must be rejected.
- **Rule 5:** The calculated SHA-256 checksum of the Payload must match the `checksum` value provided in the JSON header. If the `checksum` key is missing or mismatched, reject the chunk.

**Part 3: End-to-End Integration**
Update the worker in `/home/user/archiver/worker.py` to use your `sanitize_chunk` function. If a chunk pulled from Redis is valid, append its Payload to a master archive file at `/home/user/archiver/master_archive.bin`. If it is invalid, log the event to `/home/user/archiver/rejected.log` (one filename per line) and discard the chunk.

To test your sanitizer independently, you can evaluate it against the corpora located in:
- `/home/user/archiver/corpus/clean/`
- `/home/user/archiver/corpus/evil/`