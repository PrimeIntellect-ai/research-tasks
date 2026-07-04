You are acting as a performance engineer debugging a custom Python-based mathematical audio processing service located in `/home/user/app`. 

The service is supposed to expose an HTTP API on `0.0.0.0:8080`. It takes a POST request at `/process` containing raw audio data, transcribes the audio to extract a sequence of numbers, uses a secret seed, and computes the 100th term of a custom recurrence relation defined by the transcribed numbers.

However, the service is currently broken in multiple ways:
1. **Git Forensics**: The application requires a secret configuration salt to start, which was accidentally committed and then removed from the git history in `/home/user/app`. You must find this salt and place it in `/home/user/app/.env` as `SECRET_SALT=<salt>`.
2. **Formula Correction**: The mathematical formula implemented in `math_engine.py` for the recurrence relation has a bug. It should calculate $A_n = \alpha A_{n-1} + \beta A_{n-2} + \text{salt\_value}$, where $\alpha$ and $\beta$ are the first two numbers extracted from the audio transcription. Fix the formula.
3. **Intermittent Failure & System Calls**: The service intermittently hangs after exactly 10 requests. Use system call tracing (like `strace`) to figure out why the worker processes are deadlocking or running out of resources (hint: look at file descriptors or unclosed sockets in `server.py`). Fix the leak.

An example audio file is provided at `/app/test_audio.wav` which contains a spoken test case. You can use it to verify your math engine locally. 

Your final goal is to have the fixed service running on `0.0.0.0:8080`. The automated verifier will send HTTP POST requests with audio payloads to `http://127.0.0.1:8080/process` and expect a JSON response `{"result": <calculated_value>}`. Do not stop the server once it is running correctly.