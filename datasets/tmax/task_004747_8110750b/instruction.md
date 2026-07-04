You are an open-source maintainer reviewing a broken Pull Request for a project called `AudioMathAPI`. The project is supposed to take a sequence of spoken numbers from an audio file, merge it with user-provided numbers from a URL parameter, and return a mathematically sorted list via an Nginx reverse proxy.

The PR author has left the workspace in `/app/audio_math_api/`. It contains:
- `app.py`: A Flask application meant to run on port 8000.
- `nginx.conf`: An Nginx configuration file meant to run as an unprivileged user on port 8080.
- `transcriber.py`: A utility script that takes an audio file path and prints the transcribed numbers as text words (e.g., "nine, four, eleven").

There is a test audio file provided at: `/app/audio/test_sequence.wav`

The PR currently has several bugs that you need to fix:
1. **Nginx Reverse Proxy & Rate Limiting**: The `nginx.conf` file is supposed to listen on port `8080`, proxy requests for `/api/` to `http://127.0.0.1:8000`, and enforce a rate limit of 5 requests per second on that path. The configuration is syntactically invalid and misconfigured. Fix it.
2. **Request Validation & Routing**: The route in `app.py` is `/api/merge`. It expects two URL query parameters: `seq` (comma-separated integers) and `file` (the name of the wav file in `/app/audio/`, without the `.wav` extension). The PR author's parameter parsing is broken.
3. **Sorting & Merging**: `app.py` calls `transcriber.py` to get the spoken words from the audio file, converts them to integers, merges them with the integers from the `seq` parameter, and sorts them. However, the current code sorts the numbers alphabetically (as strings) instead of mathematically. Fix the logic so it correctly merges and sorts the integers in ascending order.
4. **Output format**: The endpoint must return a JSON response exactly in this format: `{"result": [1, 4, 5, 9, 11, 12]}`.

Your task:
- Fix the bugs in `app.py` and `nginx.conf`.
- Start the Flask backend on `127.0.0.1:8000`.
- Start Nginx using the fixed configuration (e.g., `nginx -c /app/audio_math_api/nginx.conf -p /app/audio_math_api/`).
- Leave both services running in the background so they can be verified. Ensure Nginx is listening on `0.0.0.0:8080`.