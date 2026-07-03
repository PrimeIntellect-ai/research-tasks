You are tasked with automating a backup filtering process for legacy server logs. 

As a backup administrator, you need to archive only specific multi-line log records based on dynamic configuration rules. A previous administrator wrote a compiled utility for this, but the source code was lost. A stripped binary of this utility exists at `/app/log_archiver_oracle`.

Your objective is to write a Python script at `/home/user/log_archiver.py` that perfectly replicates the behavior of the compiled utility.

The utility takes two arguments:
1. Path to a configuration file (`.ini` format)
2. Path to a log file

**Log File Format:**
- Encoded in Shift-JIS.
- Contains multi-line records separated by a line consisting exactly of `---`.
- Each record begins with a header line formatted as: `[YYYY-MM-DD HH:MM:SS] LEVEL: Source`
- Following the header is the multi-line message content.

**Configuration File Format:**
- Standard INI format.
- Contains a `[Filter]` section.
- May contain keys: `min_level` (e.g., INFO, WARNING, ERROR, CRITICAL), `source_match` (substring), and `ignore_encoding_errors` (true/false).

**Expected Output:**
Your Python script must parse the config, read the Shift-JIS encoded log file, filter the records based on the configuration, and print the matching multi-line records to `stdout` converted to strictly UTF-8 encoding. If `ignore_encoding_errors=true` is set, invalid Shift-JIS characters should be replaced with the Unicode replacement character. Otherwise, it should fail immediately (exit code 1) on encoding errors.

The `min_level` acts as a severity threshold (DEBUG < INFO < WARNING < ERROR < CRITICAL). Only records with a level greater than or equal to `min_level` should be output. If `source_match` is present, only records where the Source field exactly contains the given substring should be output.

You must implement `/home/user/log_archiver.py`. You can use `/app/log_archiver_oracle` to test your implementation. Ensure your script's output is bit-exact equivalent to the oracle utility's output for any valid input combination.