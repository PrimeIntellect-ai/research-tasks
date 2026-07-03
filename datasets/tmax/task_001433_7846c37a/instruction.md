You are a support engineer collecting diagnostics for a problematic asynchronous Python data ingestion service. The service has been crashing, producing incorrect analytics, and failing to handle unexpected payloads. 

Your goal is to fix the application's bugs, resolve its dependency issues, run a simulated workload, and extract a clean diagnostic report.

Here is the current state of the system:
The application code is located in `/home/user/app/`. 
The directory contains:
- `/home/user/app/requirements.txt`: Contains dependencies, but has a version conflict preventing installation.
- `/home/user/app/service.py`: An `aiohttp` web service that calculates an Exponential Moving Average (EMA) of incoming values. It listens on port 8080. It has a signal handler for `SIGUSR1` to dump diagnostics to `/home/user/app/diagnostics.json`.
- `/home/user/app/client.py`: A load-generator script that sends traffic to the service.

You must perform the following actions:

1. **Environment Setup**: Create a Python virtual environment at `/home/user/app/venv`. Fix the conflict in `requirements.txt` (the currently specified `numpy` version conflicts with the `pandas` version specified). Install the dependencies in the virtual environment. 
2. **Fix Formula Implementation**: Inspect `service.py`. The Exponential Moving Average (EMA) calculation is mathematically incorrect. Standard EMA should be `(Value * alpha) + (Previous_EMA * (1 - alpha))`. Correct the implementation in the code.
3. **Fix Corrupted Input Handling**: The service currently crashes with an unhandled exception when receiving malformed JSON. Modify `service.py` to catch JSON decode errors and return an HTTP 400 Bad Request response with the text `Invalid JSON` instead of crashing.
4. **Fix Concurrency Bug (Task Leak)**: The service leaks `asyncio` tasks when a client disconnects early (cancellation). Use an interactive debugger or inspect the code to find why cancelled requests leave orphaned tasks in the `active_tasks` set and keep running in the background. Patch the service so that if the request handler is cancelled, the underlying processing task is properly cancelled and removed from `active_tasks`.
5. **Run and Verify**:
   - Start `service.py` in the background using your virtual environment.
   - Run `/home/user/app/venv/bin/python /home/user/app/client.py` to simulate traffic (this will send valid requests, malformed payloads, and abort requests).
   - Once the client finishes, send a `SIGUSR1` signal to the `service.py` process.
   - This will cause the service to write `/home/user/app/diagnostics.json`.

Do not modify `client.py`. Your final output must be the `/home/user/app/diagnostics.json` file generated after the client script finishes successfully, proving that no tasks are leaked and the EMA is calculated correctly.