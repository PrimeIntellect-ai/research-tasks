You are an operations engineer triaging a critical incident in our legacy video processing pipeline. The pipeline processes user-uploaded files, but it intermittently fails and drops jobs.

We do not have traditional logs for the overarching pipeline orchestrator, but we do have a screen recording of the pipeline's monitoring dashboard during the incident window. This recording is located at `/app/incident_monitor.mp4`. When a job fails, the dashboard turns solid red and explicitly displays "FAILURE: JOB_" followed by the job ID.

Your task consists of three phases:

**Phase 1: Identify Failures**
Use `ffmpeg` and Python to process `/app/incident_monitor.mp4`. Identify all the unique Job IDs that failed during the recording. Write these failed Job IDs to `/home/user/failed_jobs.txt`, one per line, sorted numerically.

**Phase 2: Root Cause Analysis**
For every job processed by the system (failed or successful), there is an `strace` dump and an environment setup script in `/app/traces/job_<ID>/`. 
Using the failed job IDs you extracted, investigate their traces to determine the root cause of the intermittent failures. You will need to use system call tracing analysis and delta debugging to figure out what triggers the crashes. (Hint: The legacy shell scripts handling the backend processing are fragile and break on certain inputs).

**Phase 3: Write a Classifier**
Once you understand exactly what causes the jobs to fail, write a Python filter script at `/home/user/job_filter.py`. 
This script must take a single file path string as a command-line argument:
`python3 /home/user/job_filter.py "<file_path>"`

It must:
- Print exactly `ACCEPT` to stdout and exit with code 0 if the file path is safe for the legacy pipeline.
- Print exactly `REJECT` to stdout and exit with code 1 if the file path contains any characters or structures that would break the pipeline (e.g., based on the vulnerabilities you discovered in Phase 2).

We will verify your `/home/user/job_filter.py` script against a hidden test suite consisting of safe (clean) file paths and dangerous (evil) file paths designed to break the system. Your script must flawlessly accept all clean paths and reject all evil paths.