You are helping a developer organize and sanitize an old project's logs. The project logs are stored in a multi-part archive, and some of the log files have been corrupted by accidental binary dumps and fragmented records.

Your task has two phases:

**Phase 1: Build the Extractor and Unpack**
The logs are archived in a multi-part 7-Zip format at `/home/user/project_logs.7z.001` (and `.002`, etc.). However, `7z` is not installed on the system.
The source code for `p7zip_16.02` is provided as a vendored package at `/app/p7zip_16.02`. 
1. The package has a broken configuration file due to a recent bad commit. You must find and fix the compiler definition typo (a misspelled C++ compiler command) in the build configuration files so it can compile successfully.
2. Compile the package (using `make`).
3. Use the resulting `bin/7za` executable to extract the multi-part archive `/home/user/project_logs.7z.001` into the directory `/home/user/logs/`.

**Phase 2: Log Sanitization Script**
Inside the extracted logs, there are thousands of multi-line log records. Some records have been corrupted with binary data (specifically, entire ELF binaries or PNG files dumped directly into the text) or are malformed.

Write a Bash script at `/home/user/filter_records.sh` that takes a single file path as its first argument (`$1`) and outputs the sanitized log records to `stdout`. 

**Log Record Format:**
* Every valid record begins exactly with a line containing only `[RECORD_START]`
* The record spans multiple lines.
* Every valid record ends exactly with a line containing only `[RECORD_END]`

**Filtering Rules:**
Your script must output a record (including its START and END tags) ONLY IF it meets ALL of the following criteria:
1. It is correctly bounded by `[RECORD_START]` and `[RECORD_END]`.
2. It does NOT contain the ELF magic bytes (Hex: `7F 45 4C 46`, ASCII: `\x7FELF`) anywhere in its content.
3. It does NOT contain the PNG magic bytes (Hex: `89 50 4E 47`, ASCII: `\x89PNG`) anywhere in its content.

The output must exactly match the original formatting of the preserved records. No partial records or orphaned text outside of START/END blocks should be output. 

Your script will be tested against a strict adversarial corpus of "clean" and "evil" log files to ensure it correctly parses multi-line records and identifies embedded binary headers without missing edge cases.