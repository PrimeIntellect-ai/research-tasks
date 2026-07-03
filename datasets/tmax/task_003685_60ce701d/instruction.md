You are tasked with helping a backup administrator create a reliable, concurrent-safe log archiving service. We have a continuous background process that writes to log files in `/app/data/logs/` unpredictably. If we archive these files while they are being written, we get corrupted backups.

We rely on a custom, internal Python package called `pylogarchiver` (located at `/app/pylogarchiver-1.0.0`), which provides optimized streaming and file-locking primitives to safely archive actively written files. However, the package is currently broken and fails to acquire non-blocking locks correctly.

Your objectives:
1. Identify and fix the bug in the vendored `pylogarchiver` package. The bug prevents it from properly acquiring exclusive, non-blocking locks using `fcntl`. Install the fixed package into the system or virtual environment.
2. Write a Python HTTP service at `/app/server.py` that listens on `127.0.0.1:8080`.
3. The service must implement a `GET /download` endpoint. When this endpoint is accessed, the service must:
   - Recursively traverse the `/app/data/logs/` directory.
   - Use `pylogarchiver`'s `SafeArchiver` class to securely read the files (using file locking and memory-mapped I/O to avoid race conditions).
   - Generate a single compressed archive (e.g., `.tar.gz`) containing all the logs, preserving the directory structure relative to `/app/data/logs/`.
   - Return the generated archive directly in the HTTP response body with an appropriate content type (e.g., `application/gzip`).

Constraints:
- Do not stop the background writing process.
- The HTTP server must bind exactly to `127.0.0.1:8080`.
- The `SafeArchiver` class expects an output file path; you can write to a temporary file like `/tmp/backup.tar.gz` before serving it.
- Keep the service running in the background or foreground once ready, so it can be tested. Ensure your server correctly handles multiple sequential requests.