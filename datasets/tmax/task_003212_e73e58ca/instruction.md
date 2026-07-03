You are acting as a security researcher analyzing a stripped, potentially malicious binary. 

We have recovered a stripped ELF executable located at `/app/suspicious_service`. Our initial analysis indicates it is a custom network daemon that normally listens on TCP port 8000 when executed. We need to understand its protocol, identify a vulnerability within it, and create a safe mock version of the service.

Your task consists of three phases:

**Phase 1: Build Failure Diagnosis**
In `/home/user/fuzzer/`, there is a C source file `harness.c` and a `Makefile`. This harness was written by a previous researcher to test the binary's protocol, but it currently fails to build due to missing include paths and linking errors. Diagnose and fix the build failures so that `make` successfully produces a `harness` executable in that directory.

**Phase 2: Minimal Reproducible Example (MRE) Creation**
Through static analysis (e.g., `objdump`, `strings`) or by using the compiled harness to interact with the running `/app/suspicious_service`, reverse-engineer the custom TCP protocol it uses. 
We suspect there is a buffer overflow vulnerability in one of its command handlers. 
Identify the exact binary payload that causes `/app/suspicious_service` to crash with a Segmentation Fault (SIGSEGV). 
Save this exact raw binary payload to `/home/user/crash_payload.bin`. This must be the minimal reproducible example (the shortest valid protocol frame) that triggers the crash.

**Phase 3: Safe Mock Service**
Write and run a safe replacement service in any language of your choice. 
This mock service must:
1. Listen on `127.0.0.1:9090` over TCP.
2. Correctly implement the protocol parsed by the original binary, responding to its commands with the exact same binary formats that the original service used for successful requests.
3. Handle the malicious payload (from Phase 2) gracefully by returning a protocol-compliant error response instead of crashing.
4. Keep running in the background so our automated verifier can test it.

Ensure the mock service is actively listening on `127.0.0.1:9090` before you finish. The automated tests will connect to this port, speak the reverse-engineered protocol, and test both normal and adversarial inputs.