You are an on-call engineer responding to a 3 AM page. The multi-service log ingestion pipeline has started dropping log files, specifically throwing errors whenever log filenames contain spaces, newlines, or shell metacharacters.

The system is deployed in `/app/`. When running, it consists of:
1. A Redis instance acting as a message queue.
2. An HTTP webhook receiver (Python) listening on port 8080.
3. A Bash worker script that pulls from Redis and formats the filenames.

Recently, a botched Git merge in the repository at `/app/repo` replaced a robust, compiled Go helper binary with a quick-and-dirty Bash script (`/app/repo/worker/format_name.sh`). This Bash script loses precision on special characters and fails to handle corrupted inputs.

Your tasks:
1. Investigate the Git history in `/app/repo` to recover the original compiled binary (it was deleted a few commits ago).
2. Reverse-engineer what the original compiled binary did (it takes a single string as argument `$1` and outputs a specific formatted string to stdout). 
3. Write a pure Bash script at `/app/fixed_format.sh` that takes a filename as its first argument (`$1`). This script must be **bit-for-bit perfectly equivalent** in its standard output to the recovered binary for *any* possible input string, including strings with spaces, wildcards, newlines, and non-printable characters.
4. Ensure your script exits with code 0 on success, exactly matching the recovered binary.

You do not need to leave the services running at the end. Your primary deliverable is the script at `/app/fixed_format.sh`.