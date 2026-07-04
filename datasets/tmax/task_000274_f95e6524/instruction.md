As a QA engineer, you need to finalize the test environment for our new web security middleware. We are migrating our payload sanitizer from a slow Python prototype to a high-performance C binary. 

We have a multi-service architecture simulating our production environment located in `/home/user/workspace/`:
1. A frontend Node.js service (listening on port 8080).
2. A middle-tier Filter Daemon (listening on port 8081) that invokes a standalone binary to validate payloads.
3. A backend Redis cache (listening on port 6379).

Your tasks are:

1. **Code Translation & Data Encoding:**
   Read the legacy Python prototype at `/home/user/workspace/legacy_filter.py`. It reads a URL-encoded string from `stdin`, decodes it (handling `%XX` hex sequences and `+` as space), and applies security rules. 
   Write a C program at `/home/user/workspace/sanitizer.c` that exactly replicates this logic. The C program must:
   - Read up to 4096 bytes from `stdin`.
   - Perform standard URL decoding.
   - Inspect the decoded string for malicious payloads. Specifically, if the decoded string contains any of the following, it must be flagged as evil: `<` or `>`, the substring `../`, or any null byte `\0` (other than the string terminator).
   - If malicious, print exactly `REJECTED` to `stdout` and exit with status 1.
   - If clean, print exactly `ACCEPTED: <decoded_string>` to `stdout` and exit with status 0.
   Compile your code to `/home/user/workspace/sanitizer`.

2. **Test Fixture Setup & Configuration:**
   Adjust the multi-service configuration. Edit `/home/user/workspace/config.env` and change the `FILTER_BIN` variable to point to your new C binary (`/home/user/workspace/sanitizer`) instead of the legacy Python script.
   Start the multi-service environment by running the startup script: `/home/user/workspace/start_services.sh`.

3. **Adversarial Verification:**
   We have provided an adversarial test suite to ensure your C implementation is secure and doesn't introduce regressions. Run `/home/user/workspace/run_corpus_tests.sh`. This script will feed our test datasets (a clean corpus and an evil corpus) through the running Node.js frontend, which proxies through your C binary to Redis. 
   You must iteratively refine your C code until the verifier reports that 100% of the evil corpus is rejected and 100% of the clean corpus is accepted.

Once the tests pass, generate a final test report by running `/home/user/workspace/generate_report.sh`. This will create `/home/user/workspace/test_report.log`. Leave the services running and the compiled `sanitizer` binary in place.