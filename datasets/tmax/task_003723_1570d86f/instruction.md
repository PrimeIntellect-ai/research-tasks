We are migrating our internal file sorting and organization utility from a legacy Go service to a new Python-based tool. 

Your task is to implement the new tool and build a test harness for it.

Here are the requirements:

1. **Understand the Rules**: The business logic for how files should be routed to directories is documented in an architectural diagram located at `/app/routing_rules.png`. You will need to extract these rules (e.g., using OCR tools like `tesseract` which is pre-installed).
2. **Implement the Python Router**: Create a Python script at `/home/user/router.py`. It must accept a single string (the filename) as a command-line argument and print the exact target directory path to standard output (no extra newlines or text).
3. **Write a Concurrent Test Harness**: To ensure the new Python tool behaves identically to the legacy system, write an integration test harness in Go at `/home/user/tester/tester.go`. This harness must use Go concurrency patterns (goroutines and channels) to concurrently send generated test filenames to both your Python script and the legacy stripped binary located at `/app/legacy_router`. It should verify that their standard outputs match.
4. **Cross-Compilation**: We need the test harness to be portable for different developer machines. Cross-compile your Go tester for both `linux/amd64` and `linux/arm64`. Place the compiled binaries at `/home/user/bin/tester_amd64` and `/home/user/bin/tester_arm64`.

The automated verifier will strictly test your Python implementation (`/home/user/router.py`) against the legacy oracle by fuzzing it with thousands of generated filenames. It must be bit-exact equivalent.