You are an IT support technician responding to Ticket #4029. 

**Ticket Description:**
"Hi, we need to revive our old data processing pipeline located at `/home/user/legacy_pipeline`. We are facing three main issues:
1. The original developer left and accidentally deleted the production API key from the repository. We know it was committed at some point in the Git history before being removed. We need you to find it.
2. The package no longer installs. Running `pip install -e /home/user/legacy_pipeline` fails with an error. Please diagnose and fix the build issue.
3. Once installed, the `process_data` CLI tool crashes unpredictably when processing our new dataset (`/home/user/sample_data.jsonl`). We need to report this bug to the upstream vendor, so we need a Minimal Reproducible Example (MRE). Please find the exact single JSON record from the dataset that causes the crash.

**Your objectives:**
1. Find the lost API key from the Git repository's history. Write the raw API key (just the string value) to a file named `/home/user/recovered_key.txt`.
2. Fix the build error in the package so that `pip install -e /home/user/legacy_pipeline` completes successfully.
3. Write a fuzzer or iteration script to test the `process_data` command against the lines in `/home/user/sample_data.jsonl`. Identify the single JSON line that causes the tool to crash. Save ONLY this exact crashing JSON string into `/home/user/mre.json`.

Ensure your final state has the package installed, and the two output files (`recovered_key.txt` and `mre.json`) exactly as requested.