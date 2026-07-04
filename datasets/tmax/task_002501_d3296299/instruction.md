You are a QA engineer setting up a test environment for a new "Shellcode-as-a-Service" (SaaS) backend. The system allows users to submit x86_64 machine code (as hex strings) via a REST API to be analyzed and executed in a sandbox. 

Currently, the system is missing an API gateway filter to block malicious assembly instructions, and the reverse proxy isn't wired up to the backend correctly.

Your task is to:
1. Fix the `nginx` reverse proxy configuration located at `/home/user/app/nginx/nginx.conf`. It needs to listen on port 8080 and proxy requests matching the `/api/` path to the Python backend running on `127.0.0.1:5000`.
2. Enhance the Python FastAPI REST backend at `/home/user/app/api/main.py`. You must implement an assembly-level analysis filter using the `capstone` library. The endpoint `/api/execute` accepts a POST request with JSON payload `{"hex_code": "<hex_string>"}`. 
3. Your filter must disassemble the x86_64 hex string. If it contains ANY of the following instruction mnemonics: `syscall`, `int`, `int3`, or `sysenter`, the API must immediately return an HTTP 403 Forbidden with `{"error": "Malicious code detected"}`. Otherwise, it should proceed to return HTTP 200 OK with `{"status": "safe"}`.
4. Start both the Python API (using `uvicorn`) and `nginx`. 

You are provided with two test corpora to validate your filter:
- `/home/user/app/corpora/evil/`: Contains JSON files with shellcode that makes syscalls or software interrupts. Your filter MUST reject 100% of these.
- `/home/user/app/corpora/clean/`: Contains JSON files with safe shellcode (pure math/logic operations). Your filter MUST accept 100% of these.

Ensure that the dependencies (e.g., `fastapi`, `uvicorn`, `capstone`) are installed. Write your code cleanly and start the services in the background so the end-to-end flow works correctly via `http://127.0.0.1:8080/api/execute`.