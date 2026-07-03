You are a DevOps engineer tasked with debugging a log processing pipeline that has been crashing repeatedly in production.

The pipeline consists of three services running on your machine:
1. **Redis**: Running on `127.0.0.1:6379` (stores processed logs).
2. **Log Router (Python)**: Listens on `127.0.0.1:8080`. It receives raw JSON logs via HTTP POST and forwards them to the downstream processor.
3. **Log Processor (Rust binary running via Python wrapper)**: Listens on `127.0.0.1:8081`. It parses the JSON logs and stores valid entries in Redis.

**The Problem:**
The Log Processor periodically panics and crashes (dumping core/stack traces) when it encounters specific edge-case data involving bad encoding or invalid serialization formats in the payload. The service is currently configured to restart automatically, but data is being lost.

You have been provided with:
- A crash log containing a stack trace and a hex dump of the crashing memory region: `/home/user/logs/processor_crash.log`.
- A directory of sample logs that process successfully: `/home/user/corpus/clean/` (50 files).
- A directory of sample logs that trigger the crash: `/home/user/corpus/evil/` (50 files).

**Your Task:**
1. **Analyze the Crash**: Review the crash log and corpora to determine the exact structural or encoding difference that causes the processor to panic.
2. **Write a Sanitizer**: Create a Python module at `/home/user/sanitizer.py` that contains a function with the exact signature: `def is_safe(raw_bytes: bytes) -> bool`. This function must return `True` if the payload is safe to process, and `False` if it contains the malicious/crashing edge-case. Automated verification will test this function against the provided corpora.
3. **Deploy a Mitigation Proxy**: 
    - Write a simple HTTP proxy in Python at `/home/user/proxy.py` that listens on `127.0.0.1:8082`.
    - This proxy must receive HTTP POST requests, run the body through `sanitizer.is_safe()`, and if safe, forward the exact request to the Log Processor (`http://127.0.0.1:8081`). If unsafe, it should return a 400 HTTP status and drop the payload.
    - Start this proxy in the background.
4. **Reconfigure the Pipeline**: Modify the Log Router's configuration file at `/home/user/router_config.json` to forward traffic to your proxy (`http://127.0.0.1:8082`) instead of directly to the processor. 
5. **Apply Changes**: The Log Router automatically reloads its configuration when the file is modified. Ensure your proxy is running.

You must leave the proxy running and the file `/home/user/sanitizer.py` containing the `is_safe` function exactly as specified.