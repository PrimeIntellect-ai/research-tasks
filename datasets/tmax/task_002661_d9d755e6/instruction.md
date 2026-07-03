You are a build engineer responsible for maintaining a web authentication microservice. A critical security vulnerability (CVE-2024-9999) has been discovered in the underlying C shared library (`libauth`) used by our Python web application.

You need to patch the library, compile a new version, update our artifact manifest to reflect the new semantic version, and run the end-to-end test suite to verify the fix.

Here is your workflow:

1. **Apply the Security Patch**: 
   The vulnerable source code is located at `/home/user/app/src/libauth.c`.
   The patch file is located at `/home/user/app/patches/CVE-2024-9999.patch`.
   Apply this patch to the source file.

2. **Compile the Shared Library**:
   Compile the patched `libauth.c` into a new shared library named `libauth.so.1.0.1` in the directory `/home/user/app/build/`. 
   The compilation must include the `-shared` and `-fPIC` flags.
   After compiling, create a symbolic link at `/home/user/app/build/libauth.so` pointing to your newly compiled `libauth.so.1.0.1`.

3. **Update the Artifact Manifest**:
   We track library versions in `/home/user/app/manifest.json`. 
   Write a Python script at `/home/user/app/update_manifest.py` that:
   - Reads `/home/user/app/manifest.json`
   - Compares the `version` of the "libauth" component with the new version "1.0.1". You must implement basic semantic version comparison (Major.Minor.Patch) to ensure "1.0.1" > "1.0.0".
   - If the new version is strictly greater, it updates the "libauth" version in the JSON file to "1.0.1" and writes it back to `/home/user/app/manifest.json`.
   - Run this script.

4. **Run End-to-End Tests**:
   The Python web application runs a local server and connects to the shared library via `ctypes`.
   Execute the end-to-end test script located at `/home/user/app/tests/e2e_test.py`.
   This script will start the web server, send malicious payloads to test if the vulnerability is mitigated, and write a report. 
   Ensure the script executes successfully and generates the `/home/user/app/test_results.log` file containing the line "E2E SEC TEST: PASS".

Perform all these steps in the `/home/user/app` directory.