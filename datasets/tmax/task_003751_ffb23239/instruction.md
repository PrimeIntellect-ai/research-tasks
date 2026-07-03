You are an on-call engineer who just got paged at 3:00 AM. Our internal C++ data pipeline is failing. The downstream consumer is complaining that exactly one critical record was dropped during the midnight run, which caused a financial reconciliation failure.

Here is what we know:
1. The code for the pipeline is located in a Git repository at `/home/user/pipeline_repo`.
2. The pipeline consists of three phases: ingest, transform, and export. The logs for the midnight run are scattered across three files: `/home/user/logs/ingest.log`, `/home/user/logs/transform.log`, and `/home/user/logs/export.log`. 
3. A recent commit broke the timestamp boundary logic, causing a record exactly on the midnight boundary to be dropped. 
4. Rumor has it that the same developer who introduced the bug accidentally committed a plaintext secret API key in the same commit, before realizing their mistake and removing the key in a subsequent commit.

Your tasks:
1. **Log Timeline Reconstruction & Diff Analysis**: Correlate the three log files to identify the exact `record_id` of the dropped record.
2. **Git History Forensics**: Find the commit that introduced the bug. Extract the accidentally committed secret API key from the git history.
3. **Boundary Condition Repair**: Fix the off-by-one error in `/home/user/pipeline_repo/processor.cpp`. 
4. **Regression Test Construction**: Write a C++ test file at `/home/user/pipeline_repo/test_processor.cpp` that includes `processor.h`. It should test the boundary condition (processing a record exactly at `00:00:00`). When compiled via `g++ -std=c++17 test_processor.cpp processor.cpp -o test_runner` and executed, it must return an exit code of `0` if the bug is fixed, and non-zero if the bug is present.
5. **Reporting**: Create a file at `/home/user/incident_report.txt` with exactly three lines:
   - Line 1: The recovered secret API key.
   - Line 2: The full Git commit hash that introduced the bug.
   - Line 3: The `record_id` of the dropped record.