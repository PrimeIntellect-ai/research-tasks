You are a site reliability engineer investigating a severe memory leak and subsequent crash in a long-running C daemon. The daemon processes telemetry messages. Recently, a malformed message caused the service to allocate memory uncontrollably in a recursive parsing loop until the system killed it (OOM).

You have been provided with two files:
1. `/home/user/service.c`: The source code for the telemetry processing service.
2. `/home/user/memory.dump`: A raw memory dump from the crashed process just before it was terminated. 

Your task is to:
1. **Analyze the memory dump:** Extract strings from `/home/user/memory.dump` to find the exact payload that caused the crash. The malformed telemetry payload always begins with the prefix `CRASH_PAYLOAD:`. 
2. **Log the payload:** Extract the full string (including the prefix) and save it exactly as it appears into a new file at `/home/user/bad_payload.txt`.
3. **Fix the C code:** Inspect `/home/user/service.c`. You will find a function named `parse_telemetry`. There is a logic flaw causing infinite recursion and a massive memory leak when a specific payload structure is encountered. Fix the bug in `service.c` so that it terminates the recursion correctly and properly frees memory, preventing the memory leak.
4. **Compile the fix:** Compile the updated `service.c` into an executable named `/home/user/service_fixed` using `gcc`.

Ensure that when your `/home/user/service_fixed` binary is fed the malicious payload from `bad_payload.txt` via standard input, it processes it safely without hanging or crashing, returning exit code 0.