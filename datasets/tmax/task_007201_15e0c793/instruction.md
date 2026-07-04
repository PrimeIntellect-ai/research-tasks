You are a platform engineer responsible for maintaining the CI/CD pipeline of our custom Web Application Firewall (WAF) project. A recent pipeline run failed because a custom C extension used for high-speed payload parsing is causing a segmentation fault (memory safety issue) and there is a dependency conflict in the Python environment.

Your task is to fix the pipeline by completing the following steps:

1. **Fix the C Extension Memory Leak/Corruption**:
   The file `/home/user/waf_pipeline/parser.c` contains a Python C extension with a memory safety vulnerability (buffer overflow) in the `extract_payload` function. Modify the C code to safely handle inputs up to 256 bytes without overflowing the fixed-size buffer. Ensure the string is properly null-terminated.

2. **Resolve Dependencies & Build**:
   The `/home/user/waf_pipeline/requirements.txt` file has a conflicting constraint that prevents installation (it requests `requests==2.25.1` but another package requires `urllib3>=1.26.0,<1.27` while `requests==2.25.1` pins `urllib3<1.27,>=1.21.1` - wait, let's make it simpler: `Flask==2.0.1` and `Werkzeug==1.0.1` which are incompatible). Actually, just fix the `requirements.txt` so it installs successfully (upgrade Werkzeug to `>=2.0.0`). 
   Create a standard `setup.py` in `/home/user/waf_pipeline/` to compile the `parser.c` extension into a module named `waf_parser`. Build and install it in the current environment (`pip install -e .`).

3. **Implement the WAF Logic**:
   Write a Python script at `/home/user/waf_pipeline/run_waf.py`. This script must:
   - Import the fixed `waf_parser` module.
   - Read malicious signatures from `/home/user/waf_pipeline/rules.json`.
   - Implement a custom **Trie** data structure from scratch to efficiently store and search for these signatures (representing the constraint satisfaction engine).
   - Read raw payloads from `/home/user/waf_pipeline/payloads.txt` (one per line).
   - For each payload, pass it through `waf_parser.extract_payload(line)`.
   - Check the extracted payload against the Trie. If ANY signature in the Trie is found as a substring within the extracted payload, it must be blocked.
   - Write the blocked payloads to `/home/user/waf_pipeline/blocked.log` in the exact format: `[BLOCKED] <signature> IN <raw_payload>` (e.g., `[BLOCKED] admin'-- IN GET /login?user=admin'-- HTTP/1.1`). If multiple signatures match, log the first one found by your Trie's search.

Ensure your code is clean, well-structured, and handles the constraints efficiently.