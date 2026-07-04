You are a developer tasked with migrating and organizing a legacy mathematical evaluation service. The original project is currently a mess of files in `/home/user/project`, and the core evaluation logic is written in a legacy JavaScript file. You need to translate the logic to Python, organize the project into a proper modular structure, extract data from a video file, and expose an HTTP API.

**Step 1: Project Organization & Code Translation**
In `/home/user/project`, you will find `legacy_parser.js`. This script contains a custom mathematical expression parser that supports addition, subtraction, multiplication, and division, using standard precedence rules. 
1. Translate this parser into Python. Do NOT use `eval()` or `exec()` for security reasons; you must translate the parsing logic (or implement a safe AST-based evaluator that perfectly matches its behavior).
2. Organize your Python code modularly into an `app/` directory (e.g., `app/main.py`, `app/parser.py`, `app/video.py`).

**Step 2: Video Data Extraction**
There is a video artifact located at `/app/color_math.mp4`. It is exactly 10 seconds long at 10 frames per second (100 frames total). Every frame in the video consists of a uniform, solid color.
You must extract the 8-bit Red, Green, and Blue (RGB) channel values for each frame (from frame index 0 to 99). These values will serve as variables `R`, `G`, and `B` in the mathematical expressions.

**Step 3: HTTP API Implementation**
Create a Python web server (you may use Flask, FastAPI, or standard library) that listens on `127.0.0.1:8080`.
Implement a single endpoint: `POST /evaluate`
*   **Authentication:** The endpoint must require an `Authorization` header with the exact value: `Bearer MATH-TOKEN-2024`. Return HTTP `401 Unauthorized` if missing or invalid.
*   **Request Validation:** The JSON payload will look like: `{"expression": "R + G * B", "frame": 45}`. Validate that the frame index is an integer between 0 and 99. Return `400 Bad Request` if the frame is out of bounds or if the expression contains unrecognized variables (only `R`, `G`, `B`, numbers, and `+-*/` are allowed).
*   **Evaluation:** Using the extracted RGB values from the requested frame, evaluate the expression using your translated parser.
*   **Rate Limiting:** Implement rate limiting mapped by client IP. A single IP may make a maximum of 5 requests per second. Any request exceeding this limit must immediately return HTTP `429 Too Many Requests`.
*   **Response:** On success, return HTTP `200 OK` with JSON `{"result": <float_value>}`.

Ensure your server is running in the background and listening on `127.0.0.1:8080` when you consider the task complete. You may write logs to stdout or files as you see fit.