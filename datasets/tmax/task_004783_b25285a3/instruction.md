You are a platform engineer maintaining a local CI/CD environment. Our automated test suite requires a mock version of our legacy Audio Feature Extraction service. The service wraps an old C library, stores metadata in an SQLite database, and exposes a REST API.

Your task is to build and run this mock service using Python.

Step 1: Build the C Library (FFI)
In `/app/src/`, you will find `libaudiofeat.c`. Compile this into a shared object library named `libaudiofeat.so` in the `/app/bin/` directory.
The C function signature is: `float get_audio_feature(const char* filepath);`
Write a Python wrapper in `/app/service/ffi_wrapper.py` that uses the `ctypes` module to call this function.

Step 2: Schema Migration
You must initialize an SQLite database at `/app/data/ci_service.db`.
In `/app/migrations/`, there are two SQL files: `001_init.sql` and `002_add_columns.sql`. Apply them in order to create the `jobs` table and add the necessary columns.

Step 3: Build the API (Routing)
Create a Python web service (e.g., using Flask, FastAPI, or standard library) in `/app/service/server.py`. It must listen on `127.0.0.1:8080`.
Implement the following routes:
- `POST /process`: Accepts a JSON payload `{"filepath": "<path_to_audio_file>"}`. 
  1. Calls your Python FFI wrapper on the provided filepath.
  2. Inserts a new row into the `jobs` table with the filepath, the returned feature value, and status `"COMPLETED"`.
  3. Returns JSON: `{"job_id": <the_inserted_row_id>}`.
- `GET /job/<job_id>`: Returns JSON data for the given job: `{"id": <job_id>, "filepath": "...", "feature_value": <float>, "status": "COMPLETED"}`. Return a 404 status code if the job does not exist.

Step 4: Run the Service
Ensure your server is running in the background and listening on `127.0.0.1:8080`. Write a log of the server's output to `/app/logs/server.log`.

For testing, an audio fixture is provided at `/app/test_audio.wav`. You can verify your system works by manually curling your local endpoints.