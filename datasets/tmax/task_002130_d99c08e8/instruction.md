You are an artifact manager tasked with curating a repository of compressed configurations and binaries. Our new system relies on an upload service, a queue, and a worker daemon, but the stream processing logic is missing.

Your objectives are:
1. Write a Python script at `/home/user/process_artifact.py`.
   - The script must accept a single command-line argument: the absolute path to a gzip-compressed file.
   - It must read and decompress the file contents.
   - It must perform large-scale text editing: replace every occurrence of the exact string `__MACRO_REPO_HOST__` with `artifact-repo.internal.srv`.
   - It must re-compress the modified contents using gzip (default compression level).
   - It must save the result back to the original file path **atomically**. (You must write to a temporary file in the same directory first, then replace the original file to ensure concurrent readers never see a partial file).

2. Integrate and start the multi-service stack.
   - The system resides in `/app/`. It consists of a Redis server (port 6379), a Flask upload service (`/app/upload_server.py`, port 5000), and a worker daemon (`/app/worker.py`).
   - The worker daemon is started via `/app/start_worker.sh`. You must modify `/app/start_worker.sh` to set the environment variable `PROCESSOR_SCRIPT=/home/user/process_artifact.py` so the worker knows which script to invoke.
   - You must start Redis, the Flask upload service in the background, and the worker daemon in the background.

Verify your setup: if you send a gzipped text file to `http://127.0.0.1:5000/upload`, it should be processed by your script via the worker.