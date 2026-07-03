You are helping me debug a regression in a locally vendored package. 

We have a local vendored package located at `/app/fin_calc-1.2.0`. This directory is a git repository containing exactly 200 commits. The package provides a simple HTTP API for financial calculations.

However, a few issues have cropped up recently:
1. **Build Failure:** The `Makefile` in the current `HEAD` is broken and fails when you run `make install`. You need to diagnose and fix this so you can run the application.
2. **Floating-point Precision Regression:** A regression was introduced somewhere in the last 200 commits. The `/variance` endpoint is returning slightly inaccurate floating-point results due to native float handling instead of exact Decimal calculations. You need to identify the issue (you may bisect the repository to find when it broke) and fix the precision logic in `app.py` so it strictly uses the Python `decimal` module for all calculations to avoid floating-point drift.
3. **Corrupted Input Handling:** The `/variance` endpoint currently crashes (returns 500) if the input JSON array contains corrupted/non-numeric strings (e.g., `"1.1a"`). You need to add recovery logic to catch these parsing errors and gracefully return an HTTP 400 status with the JSON response `{"error": "corrupted input"}`.

Your task:
1. Fix the build script.
2. Fix the floating-point precision issue in `app.py`.
3. Fix the corrupted input handling in `app.py`.
4. Start the server. The server must run on `127.0.0.1:8080` (you can run `python app.py` or similar, ensure it binds to this address and port).
5. The server must continue to enforce its existing authentication (requiring the header `X-Auth-Token: super-secret-token-99`).

Leave the fixed server running in the background. My automated test suite will send HTTP POST requests to `127.0.0.1:8080/variance` to verify the exact precision and error handling.