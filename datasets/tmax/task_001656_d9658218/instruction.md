You are an IT support technician specializing in forensic analysis. Our department uses a custom Python web service to analyze recovered voicemail audio files. The source code is located in `/home/user/voicemail_analyzer/`. 

Recently, the service has been failing, and several tickets have been raised. You need to debug and fix the application, then deploy it.

Here are the reported issues:
1. **Crash on specific files**: The custom WAV parser in `wav_parser.py` crashes with a `KeyError` or `StructError` when processing audio files that contain non-standard chunks (like `fact` or `JUNK` chunks) before the `data` chunk. You need to repair this edge-case so it correctly skips unknown chunks.
2. **Infinite Loop / Recursion**: The silence detection algorithm in `analyzer.py` (`trim_silence` function) throws a `RecursionError` on long files. You must rewrite or fix this logic to terminate correctly without exceeding the recursion limit.
3. **Floating-point precision**: The audio duration is currently calculated by accumulating the duration of tiny chunks. This causes floating-point precision loss, leading to inaccurate results. Fix it to calculate the exact duration using total frames and the frame rate.
4. **Service Error**: The Flask app in `app.py` has a bug where it fails to parse the uploaded file correctly due to a traceback in the multipart form handling.

Your task:
1. Read the traceback logs in `/home/user/voicemail_analyzer/logs/error.log` (if any, or generate them by running the app) to diagnose the issues.
2. Fix the Python code in `/home/user/voicemail_analyzer/`.
3. Start the Flask service so it listens on `0.0.0.0:8000`. It must accept `POST` requests at the `/analyze` endpoint. The payload will be a multipart/form-data request with a file field named `audio`. The expected response is a JSON object: `{"duration": <float>, "samples": <int>, "status": "success"}`.
4. There is a corrupted audio file at `/app/evidence.wav`. You must process this file through your fixed service. To prove it works, save the JSON response from the server for this specific file to `/home/user/evidence_result.json`.

Ensure your service remains running in the background on port 8000 so our automated verifier can test it with additional audio files.