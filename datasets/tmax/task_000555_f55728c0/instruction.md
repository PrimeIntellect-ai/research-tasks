You are a web developer migrating a legacy analytics processing feature for a web backend. The original implementation (`/home/user/app/legacy_processor.py`) was meant to fetch JSONL access logs via HTTP, filter out error requests, and aggregate usage statistics. However, a severe architectural flaw (a circular import between `legacy_processor.py` and its helper modules) currently prevents it from even running. 

Your task is to completely replace this broken Python script with a robust Bash pipeline, apply a patch to update the test suite's expectations, and write an end-to-end test orchestrator.

Here are your specific objectives:

1. **Code Translation (Bash Data Processing):**
   Create a new script at `/home/user/app/process_metrics.sh`.
   - It must accept a single argument: an HTTP URL pointing to a JSONL log file.
   - It must fetch the JSONL file using `curl`.
   - It must parse the JSON lines (you may use `jq`), keeping only records where the numeric `status` field is strictly less than `400`.
   - It must aggregate the `path` field, counting the occurrences of each path.
   - It must output the results to standard output in the format `path,count` (e.g., `/api/login,5`), sorted strictly by the count in descending numerical order. If counts are tied, sort alphabetically by path.
   - Ensure the script is executable.

2. **Diff and Patch Processing:**
   The product requirements for the output format recently changed, but the static expected test data wasn't updated manually. 
   - A patch file exists at `/home/user/app/tests/format_update.patch`.
   - Apply this patch to `/home/user/app/tests/expected.txt` so the test suite reflects the correct new formatting requirements.

3. **End-to-End Test Orchestration:**
   Write an E2E orchestration script at `/home/user/app/run_e2e.sh`. The script must:
   - Start a local HTTP server in the background (e.g., using `python3 -m http.server 8000`) serving the directory `/home/user/app/data/`.
   - Wait for the server to be fully ready to accept connections.
   - Execute `/home/user/app/process_metrics.sh http://localhost:8000/access.jsonl` and redirect its standard output to `/home/user/app/tests/actual.txt`.
   - Shut down the background HTTP server process safely.
   - Compare `/home/user/app/tests/actual.txt` with `/home/user/app/tests/expected.txt`.
   - Exit with code `0` if they match exactly, and a non-zero exit code if they differ.
   - Ensure the script is executable.

Your final verification will be running `/home/user/app/run_e2e.sh` which should succeed and exit with code 0.