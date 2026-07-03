You are a web developer building a new feature for a video analytics platform. We need a REST API that allows users to submit custom scripts written in a proprietary Domain Specific Language (DSL) called "VidScript". This DSL is designed to extract pixel data and count events from video files.

Your task is to build a Python-based backend service using FastAPI that implements request validation, a custom VidScript interpreter, and a rate limiter.

Requirements:

1. **VidScript Interpreter**
You must implement an interpreter for VidScript. The interpreter operates on a video file located at `/app/video.mp4` (a 30 FPS video). The interpreter has 4 registers (`R0`, `R1`, `R2`, `R3` initialized to 0) and processes the following commands:
- `SEEK <frame>`: Jump to a specific frame number in the video.
- `LUM <x> <y> <reg>`: Calculate the grayscale luminance (0-255) of the pixel at (x, y) in the current frame and store it in `<reg>`. (Luminance = 0.299*R + 0.587*G + 0.114*B).
- `ADD <reg1> <reg2>`: Add the value of `<reg2>` to `<reg1>`.
- `JGT <reg> <val> <line>`: Jump to line number `<line>` (0-indexed) if `<reg>` > `<val>`.
- `RET <reg>`: Stop execution and return the value of `<reg>`.

2. **API Endpoint & Rate Limiting**
Create a FastAPI app running on port 8000.
- Endpoint: `POST /execute`
- Payload: `{"script": "VidScript string", "client_id": "string"}`
- Validation: Return 400 if the script contains invalid commands.
- Rate Limiting: Implement an in-memory token bucket rate limiter. Each `client_id` is allowed a maximum of 3 requests per minute, regenerating 1 token every 20 seconds. Return 429 Too Many Requests if the limit is exceeded.
- Response on success: `{"result": <integer value from RET>}`

3. **Performance & Testing**
Write a unit test suite using `pytest` in `/home/user/tests/test_api.py` that verifies the rate limiter and the interpreter logic. Your code must be efficient. The video frame extraction should not re-open the file from scratch for sequential `SEEK` commands if possible.

Create the FastAPI application in `/home/user/app.py`. Ensure it can be started with `uvicorn app:app --port 8000`. You do not need to start the server manually in the final state, but the code must be fully ready to run.