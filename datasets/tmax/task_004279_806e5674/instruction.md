You are a security researcher analyzing a suspicious Python web service that was discovered on a compromised machine. The service code is located at `/app/server.py`, but it is currently unstable and crashes when handling certain edge-case data.

We have also recovered two forensic artifacts from the compromised machine:
1. An image file at `/app/clue.png`. You must use OCR (`tesseract` is preinstalled) to extract a hidden system override code from this image. The text will be in the format `SYSTEM_OVERRIDE_CODE=<code_here>`.
2. A partial process memory dump at `/app/memory.dmp`. You must perform memory dump analysis and string extraction to find an active debug session ID. Look for a string in the format `DEBUG_SESSION_ID=<id_here>`.

Your objectives are:
1. Analyze and debug `/app/server.py`. It currently crashes with an unhandled exception when it receives requests lacking specific headers. You must fix the code so that it gracefully handles missing or malformed headers by returning an HTTP 400 status code, rather than crashing.
2. Update the `/status` endpoint in `/app/server.py` to require authentication. If a GET request to `/status` includes the headers `X-Override-Code` (matching the code from the image) and `X-Session-Id` (matching the ID from the memory dump), it should return an HTTP 200 status code and the JSON payload `{"status": "recovered"}`.
3. Start the fixed service so it listens on `127.0.0.1:8000`. Ensure the service is running in the background and is ready to accept connections before you finish the task.

Do not change the endpoint path or the expected response payload. The automated verifier will send HTTP requests to test both the stability of your fix (sending malformed requests) and the accuracy of your forensic extraction (sending the correct credentials).