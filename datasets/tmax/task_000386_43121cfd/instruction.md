You are an integration developer building a custom API for a retro-computing emulator service. 

We have received a specification document as an image located at `/app/arch.png`. This image contains the architectural specifications for our new "RetroAPI" service, including the assembly instruction set it must support, the available registers, and strict API rate limiting rules.

Your task is to:
1. Extract the specification details from `/app/arch.png` (you may use tools like `tesseract` to read it).
2. Create a Python web server named `/home/user/server.py` (using FastAPI, Flask, or any standard framework) that listens on `127.0.0.1:8000`.
3. The server must expose a `POST /run` endpoint that accepts a JSON payload: `{"asm": "<assembly code string>"}`.
4. Implement the custom emulator/interpreter inside the server based on the instruction set found in the image.
5. The `POST /run` endpoint should return a JSON response with the final state of all registers. For example: `{"r0": 10, "r1": 0, "r2": 5, "r3": 0}`. All registers should initialize to `0` at the start of a program execution.
6. Implement request validation and the exact rate limiting specified in the image. If the rate limit is exceeded, the server must return a `429 Too Many Requests` HTTP status code.
7. Start your server in the background so it is actively listening on port 8000 when you complete the task.

Ensure your emulator accurately processes the opcodes, handles sequential execution correctly, and strictly adheres to the rate limiting rules. You can use standard Python libraries or install any packages you need via pip.