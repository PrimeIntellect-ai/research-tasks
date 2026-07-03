As an operations engineer, you are tasked with triaging a severe incident involving our internal telemetry parsing service. The service recently crashed in production, leaving behind a core dump. 

We have the following artifacts available:
1. A stripped binary of the deployed service at `/app/telemetry_parser`.
2. The core dump generated during the crash at `/app/crash.core`.
3. The original (but slightly broken) source code repository in `/home/user/src`.

Your objectives are:
1. **Analyze the core dump** to extract the crashing payload and determine what input caused the fault. 
2. **Fix the build failures** in `/home/user/src`. The code currently fails to compile and link due to missing headers and unlinked libraries. You must diagnose and resolve these build errors.
3. **Patch the vulnerability**: Identify the buffer overflow vulnerability in the C source code that gets triggered by the crashing payload, and patch it so that the service can safely handle arbitrarily long inputs without crashing or truncating in a way that breaks the expected output format.
4. **Build the patched service**: Compile your fixed code and save the final executable exactly at `/home/user/telemetry_parser_fixed`.

The telemetry parser reads lines from standard input and prints parsed JSON to standard output. Your patched binary must exactly match the benign output behavior of the original binary, but safely handle (e.g., truncate safely or gracefully ignore) malicious inputs without crashing.

**Evaluation:**
We will test `/home/user/telemetry_parser_fixed` using an automated verification script that feeds it 1000 test cases (a mix of benign logs and malicious oversized logs). 
The metric used is the `success_rate`, which is the fraction of inputs correctly parsed or safely handled without crashing. You must achieve a `success_rate` of `1.0` (100%).