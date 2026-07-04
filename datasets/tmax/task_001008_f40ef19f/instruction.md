You are acting as a storage administrator responsible for managing disk space on a heavily utilized database server. We are running low on disk space due to an accumulation of Write-Ahead Log (WAL) files. You need to write a Bash script to parse, filter, and highly compress these logs.

Your task consists of two main parts:

**Part 1: Toolchain Preparation**
We require extremely fast and efficient compression, so we use `pigz` (Parallel gzip). Its source code is vendored locally in `/app/pigz-2.8`.
1. Navigate to `/app/pigz-2.8` and compile the package. 
2. The compilation currently fails due to a configuration error left by a previous admin. You must identify and fix the perturbation in the build configuration (Makefile) so that it compiles successfully using the standard `gcc` compiler.
3. Once compiled, use the resulting `pigz` binary for Part 2.

**Part 2: Log Archival Script**
Write a Bash script at `/home/user/process_logs.sh` that performs the following steps:
1. Parse the configuration file at `/home/user/archiver.conf`. This file contains key-value pairs (e.g., `LOG_DIR=/home/user/wal_logs`).
2. Traverse the directory specified by `LOG_DIR`.
3. Evaluate every file in the directory. A file should ONLY be archived if it is a valid WAL file. A valid WAL file is defined by its domain-specific magic bytes: the first 4 bytes of the file must exactly match the hex signature `57 41 4C 5F` (which translates to the ASCII string `WAL_`).
4. Tar all valid WAL files and pipe them into your compiled `pigz` binary.
5. You must configure `pigz` to use the maximum possible compression level to save disk space.
6. The final compressed archive must be saved exactly at `/home/user/final_archive.tar.gz`.

**Requirements & Constraints:**
- Your script `/home/user/process_logs.sh` must be written in Bash.
- Ensure the script is executable.
- Run your script to generate `/home/user/final_archive.tar.gz`.
- The success of this task will be evaluated by an automated verifier that checks the file size of your final archive. To pass, the archive must contain all valid WAL files, exclude all invalid ones, and the final file size must strictly meet our compression threshold metric.