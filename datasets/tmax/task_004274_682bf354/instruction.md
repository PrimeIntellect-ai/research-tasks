You are a platform engineer tasked with repairing a broken CI/CD test pipeline for a new audio processing microservice. 

The pipeline is currently failing due to several issues: a package dependency conflict preventing the test environment from building, a missing reverse proxy configuration, and an incomplete mock backend required for integration testing.

Your objectives are to fix the environment, configure the proxy, implement the mock API, and successfully run the integration test.

**Step 1: Resolve Dependency Conflicts**
In `/home/user/project/requirements.txt`, there are conflicting peer dependencies (e.g., incompatible versions of `Flask`, `Werkzeug`, or `urllib3` vs `requests`). Fix the `requirements.txt` file so that `pip install -r requirements.txt` succeeds without errors. You may upgrade or downgrade versions as needed, but you must include `Flask`, `pytest`, `requests`, `numpy`, and `scipy`.

**Step 2: Configure the Reverse Proxy**
The test suite assumes the API sits behind an Nginx reverse proxy. 
Create an Nginx configuration file at `/home/user/project/nginx.conf`. It must:
- Listen on port `8000`.
- Proxy all requests to the backend Python API running on `127.0.0.1:5000`.
- Be runnable via `nginx -c /home/user/project/nginx.conf` (ensure you set appropriate pid and temp paths if running as a non-root user).

**Step 3: Implement the Mock Audio API**
Write a Python REST API in `/home/user/project/api.py` (using Flask or any framework you installed). 
- It must run on port `5000`.
- It must expose a `POST /process` endpoint.
- The endpoint should accept a WAV file uploaded via `multipart/form-data` with the field name `audio`.
- The API must read the WAV file, apply a Peak Volume Normalization so that the peak amplitude of the audio exactly equals **-3.0 dBFS** (relative to the maximum possible value for a 16-bit PCM WAV, which is 32768).
- The endpoint must return the normalized 16-bit PCM WAV file as an attachment/byte stream.

**Step 4: Create the Test Fixture & Run Tests**
Write a test script at `/home/user/project/test_api.py`.
- It should use `pytest`.
- It must contain a test fixture that sends the sample audio file located at `/app/audio/sample.wav` to `http://localhost:8000/process` using the `requests` library.
- It must save the response from the API to exactly `/home/user/project/processed_audio.wav`.

Execute your test suite to ensure the entire flow works (Nginx -> API -> Processed output). Leave the resulting `/home/user/project/processed_audio.wav` on disk for final verification.