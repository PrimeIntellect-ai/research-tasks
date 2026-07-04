You are an IT support technician acting as a Tier 3 escalation engineer. We have a high-priority ticket (Ticket #4092) regarding an internal Python microservice that periodically crashes with `UnicodeDecodeError` and severe Memory Exhaustion (OOM) errors.

A recent crash produced a partial memory dump before the service died. The ticket states that the service processes a custom binary serialization protocol, and a malformed payload is causing the crash.

Your objectives are to analyze the dump, fix the underlying vulnerabilities in the deserialization code, and write a regression test.

**Environment details:**
- Working directory: `/home/user/ticket_4092`
- Files provided (already exist):
  - `processor.py`: Contains the `deserialize(data: bytes)` function used by the service.
  - `memory.dmp`: A simulated binary memory dump taken right before the last crash. The application logs the last processed payload in memory with the string prefix `CRASH_CONTEXT:` followed by a Base64-encoded string representing the raw bytes of the crashing payload.

**Task Instructions:**
1. **Memory Dump Analysis**: Extract the base64-encoded payload from `/home/user/ticket_4092/memory.dmp` that immediately follows the `CRASH_CONTEXT:` marker.
2. **Decode and Document**: Decode the base64 payload into raw bytes. Write the exact hexadecimal representation of these raw bytes to `/home/user/ticket_4092/extracted_payload.txt` (just the hex string, no newlines or other text).
3. **Troubleshoot Encoding & Fix**: Modify `processor.py` to fix two critical vulnerabilities:
   - **Memory Exhaustion**: In the `CUST` protocol handler, if the requested payload `length` is strictly greater than `1000`, it must immediately raise a `ValueError("Payload too large")`.
   - **Encoding Crash**: The UTF-8 decoding step must not crash on invalid bytes. Update it to gracefully handle invalid sequences by replacing them (e.g., using Python's built-in error replacement strategy).
4. **Regression Testing**: Create a `pytest` test file at `/home/user/ticket_4092/test_processor.py`. 
   - Write a test function named `test_regression_cve_2023_memory()`.
   - The test must pass the exact raw crashing bytes (from step 2) to the `deserialize` function.
   - The test must assert that a `ValueError` with the message `"Payload too large"` is raised, proving the vulnerability is mitigated.

Ensure your code is correct and the test passes when `pytest /home/user/ticket_4092/test_processor.py` is executed.