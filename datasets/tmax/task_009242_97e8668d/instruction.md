Wake up! It's 3:00 AM and the on-call pager is going off. The data ingestion pipeline is dropping critical payloads and returning obscure error codes. The team relies on a legacy bash script pipeline located at `/home/user/data_pipeline`, which integrates with a compiled helper binary. 

You need to investigate the repository, find out what broke, recover lost credentials, and determine the exact edge-case payload causing the crash.

Your objectives:
1. **Git Forensics:** The pipeline requires a fallback API key that was accidentally committed and subsequently removed from the repository's history in the past. Find this deleted API key.
2. **Binary Inspection:** The pipeline uses a compiled binary `payload_decoder` in the repository. It's undocumented, but it requires a specific hardcoded master password to execute properly. Reverse engineer/inspect this binary to find the master password.
3. **Regression Bisection:** Use `git bisect` to identify the exact commit that introduced the current pipeline failure. The pipeline works perfectly in the initial commit, but fails on the `main` branch HEAD. A test script `test_pipeline.sh` is provided in the repo; the bad commit causes the pipeline to exit with a non-zero code for standard inputs.
4. **Fuzz Testing:** Even before the regression, there was a hidden bug. Write a simple bash fuzzer to pass random 4-character alphabetical strings to the initial working version of `pipeline.sh`. Find the exact 4-character string that causes `pipeline.sh` to trigger a "FATAL_EXCEPTION" output.

Once you have gathered this information, create a precise report at `/home/user/incident_report.txt` with the following format (each on a new line):
BAD_COMMIT_MSG=<The exact commit message of the commit that broke the pipeline>
RECOVERED_API_KEY=<The API key found in git history>
BINARY_PASSWORD=<The hardcoded password found in the compiled binary>
CRASHING_PAYLOAD=<The 4-character string that crashes the script>