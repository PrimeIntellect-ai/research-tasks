You are tasked with investigating a critical issue in a long-running data processing service. The service has been experiencing memory leaks and occasionally hangs completely (deadlocks) under high contention. You need to resolve its environment, extract leaked secrets from a memory dump, and write a fuzzer to reproduce the deadlock.

All service files are located in `/home/user/service/`.

**Phase 1: Dependency Conflict Resolution**
The project dependencies in `/home/user/service/requirements.txt` are currently broken. If you install them and try to run `python3 /home/user/service/app.py`, it will fail with an `ImportError`. 
Identify and resolve the dependency conflict by modifying `requirements.txt`. Create a virtual environment at `/home/user/service/venv`, install the working dependencies, and ensure `app.py` can run without immediate import errors.

**Phase 2: Memory Dump Analysis and String Extraction**
The service recently crashed due to OOM (Out of Memory). A core dump has been collected and is available at `/home/user/service/core.dmp`. 
Due to a known memory leak, an unencrypted secret key was left in the heap before the crash. Analyze the raw memory dump file and extract this key. The key is wrapped in a specific format: `SECRET_KEY_BEGIN_<base64_encoded_string>_END`.

**Phase 3: Fuzz Testing to Reproduce Deadlock**
The `app.py` exposes a function `process_payload(payload: str)`. We know there is a specific short payload string (between 5 and 10 characters) that causes the function to enter an infinite loop / deadlock state. 
Write a fuzz testing script in Python (e.g., at `/home/user/service/fuzzer.py`) to call `process_payload(payload)` with various inputs until you discover the exact string that causes it to hang indefinitely. (Note: the function normally returns `True` for valid payloads and `False` for invalid ones, but hangs on the poison payload).

**Deliverables**
Create a JSON file at `/home/user/investigation.json` with exactly the following structure:
```json
{
  "fixed_markup_safe_version": "x.y.z",
  "leaked_secret_key": "SECRET_KEY_BEGIN_..._END",
  "deadlock_payload": "..."
}
```
Replace the values with:
1. The version of `MarkupSafe` you settled on to resolve the `Flask` import conflict.
2. The exact secret key string extracted from the memory dump.
3. The exact payload string discovered by your fuzzer that causes the deadlock.