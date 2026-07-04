You are an operations engineer triaging a critical incident on our log-processing server. A legacy log parsing utility recently crashed in production, causing downstream system outages due to malformed logs simulating a buffer overflow payload. During the panic, a junior engineer accidentally deleted the recovered crash logs.

Your task consists of three phases:

**Phase 1: Fix the Vendored Package**
We vendor a third-party bash utility suite under `/app/vendored/bash-log-utils-1.4.0`. It contains a script called `process_entry.sh`. However, it is currently broken:
1. It fails to run due to a local environment variable conflict (a dependency conflict with an outdated `awk` wrapper alias set in `/app/vendored/bash-log-utils-1.4.0/env_setup.sh`).
2. Once the environment is fixed, running it on certain inputs causes an infinite recursion bug, freezing the system. 
You must fix both issues within the vendored package so that `process_entry.sh` runs successfully and terminates on all inputs.

**Phase 2: Recover Deleted Logs**
The deleted crash logs were moved to a pseudo-filesystem structure under `/tmp/fs_recovery_img/`. You must inspect the simulated block pointers in `/tmp/fs_recovery_img/inode_table.txt` to reconstruct the deleted file `crash_evidence.log` and place it at `/home/user/crash_evidence.log`.

**Phase 3: Create a Sanitizer Filter**
You must write a Bash script at `/home/user/sanitize.sh` that reads log lines from standard input and writes them to standard output. 
The script must use the fixed `process_entry.sh` internally. It must filter out any "evil" log entries that contain the buffer overflow trigger pattern (identified as any string with more than 50 consecutive hexadecimal characters, or sequences known to cause numerical instability in our downstream parser: explicitly the string `0xNaN` or `infinity_loop_ptr`). Normal log lines should be preserved and output unchanged.

Your script will be tested against two corpora:
- Clean corpus: Standard production logs.
- Evil corpus: Incident logs containing the crash payloads.

Your script must exit with code 0. Please leave `/home/user/sanitize.sh` executable.