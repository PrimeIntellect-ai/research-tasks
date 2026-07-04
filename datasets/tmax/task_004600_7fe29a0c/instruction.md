We have a legacy video analysis daemon written in Bash located at `/home/user/app/video_server.sh`. This service listens for HTTP GET requests to extract frames from a surveillance video (`/app/surveillance.mp4`) and serves them as Base64-encoded JSON, alongside a reconstructed access log timeline. 

Recently, we've noticed two critical issues:
1. **Memory Leak**: When left running, the service consumes increasing amounts of RAM until the OOM killer terminates it. This seems to happen when processing many frame extraction requests.
2. **Incorrect Log Timeline**: When querying the `/logs?start=<ts>&end=<ts>` endpoint, the reconstructed timeline omits some logs and orders others incorrectly. The system processes microsecond-precision timestamps, but a bug (likely a 32-bit signed integer overflow in the Bash math context) causes incorrect timeline reconstruction for large timestamp values. Furthermore, the JSON serialization for the logs endpoint frequently generates invalid JSON due to unescaped control characters.

Your task:
1. Diagnose and fix the memory leak in `/home/user/app/video_server.sh` without changing its core dependencies (it uses `nc` and `ffmpeg`).
2. Fix the integer overflow issue in the log timeline reconstruction logic so that microsecond timestamps are correctly compared and ordered.
3. Fix the JSON serialization issue so that the `/logs` endpoint always returns strict, valid JSON.
4. Write a regression test script at `/home/user/app/regression_test.sh` that sends 100 requests to `/frame?ts=0.5` and verifies that the memory usage of the daemon does not grow by more than 5MB. The script should exit with 0 on success and 1 on failure.
5. Finally, start the fixed daemon so it listens on `127.0.0.1:8080` and leave it running in the background.

The daemon must support the following HTTP endpoints precisely:
- `GET /frame?ts=<seconds>`: Must return HTTP 200 with `Content-Type: application/json` and body `{"time": <seconds>, "image": "<base64_of_extracted_jpeg_frame>"}`.
- `GET /logs?start=<micros>&end=<micros>`: Must return HTTP 200 with valid JSON representing the chronologically ordered array of access logs between the start and end microsecond timestamps.

Do not switch the primary language of the daemon; it must remain in Bash.