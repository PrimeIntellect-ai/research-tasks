You are an edge computing engineer deploying a new data processing pipeline for IoT sensor devices. 

We have a proprietary, stripped binary located at `/app/sensor_parser`. This binary parses raw binary telemetry files sent from edge devices. Unfortunately, the binary is brittle: certain malformed payloads cause it to segfault and crash the entire processing pipeline. We cannot modify the binary.

We have captured samples of both good and bad telemetry data:
- `/app/corpus/clean/`: Contains typical, valid sensor payloads.
- `/app/corpus/evil/`: Contains malformed payloads that crash the `/app/sensor_parser` binary.

Your task is to build a robust deployment wrapper around this binary:

1. **Investigate and Build a Validator:**
   Analyze the provided binary and corpora to determine the structural flaw causing the crashes. Write a standalone validation script located at `/home/user/validate_payload` (you may use Python, Bash, Perl, etc.).
   - It must take a single argument: the path to a payload file.
   - It must exit with code `0` if the payload is safe/clean.
   - It must exit with a non-zero code (e.g., `1`) if the payload is malformed/evil.

2. **Setup Spool Directories & Permissions:**
   Create the following directory structure for the processing pipeline:
   - `/home/user/spool/incoming/`
   - `/home/user/spool/processed/`
   - `/home/user/spool/quarantine/`
   Set the permissions of `/home/user/spool/incoming/` to exactly `733` (`drwx-wx-wx`), which allows external unprivileged sync processes to drop files into the directory without being able to list its contents.

3. **Create a Supervisor Script:**
   Write a script at `/home/user/supervisor.sh` that acts as a simple process supervisor. When run, it should:
   - Iterate over any files currently in `/home/user/spool/incoming/`.
   - Run `/home/user/validate_payload` on each file.
   - If the file is valid, run `/app/sensor_parser <file>`, redirect the standard output to a file of the same name in `/home/user/spool/processed/`, and delete the incoming file.
   - If the file is invalid, move it directly to `/home/user/spool/quarantine/` without running the parser.

Focus entirely on getting `/home/user/validate_payload` perfectly accurate. Ensure it relies on the internal structure of the files, not just matching known filenames.