You are tasked with building a robust anomaly detection pipeline for our fleet of IoT edge servers. These servers regularly upload configuration change logs as time-series data. Recently, an attacker has been injecting malicious configurations and executing "configuration flood" attacks to destabilize the network.

Your goal is to write a Bash-only script located at `/home/user/classifier.sh` that takes a single file path as an argument and classifies it as either "clean" (exit code 0) or "evil" (exit code 1).

### Input Format
Each input file is a CSV (without a header) representing a time-series of configuration changes.
The columns are: `Timestamp,DeviceID,PayloadEncoding,ConfigPayload`
Example line:
`2023-10-14T15:30:00Z,EDGE-99,base64_utf16le,SABlAGwAbABvAA==`

The `PayloadEncoding` column will be either:
- `plain_utf8`: The `ConfigPayload` is a raw UTF-8 string.
- `base64_utf8`: The `ConfigPayload` is base64 encoded; when decoded, it is UTF-8.
- `base64_utf16le`: The `ConfigPayload` is base64 encoded; when decoded, it is UTF-16LE.

### Rules for Classification
A file is considered "evil" (and must be rejected with exit code 1) if it violates **ANY** of the following rules. Otherwise, it is "clean" (exit code 0).

1. **Payload Content Validation:**
   We have a legacy, stripped proprietary security validation binary located at `/app/config_checker`. 
   For every line in the file, you must decode and normalize the `ConfigPayload` into a standard UTF-8 string. You must then pass this decoded UTF-8 string to the `/app/config_checker` binary via standard input. 
   If `/app/config_checker` exits with a non-zero status for *any* payload in the file, the entire file is "evil".

2. **Configuration Flood Detection (Aggregation):**
   You must normalize the `Timestamp` (which is in ISO 8601 UTC format) to determine the hour of the event.
   If any single `DeviceID` registers more than 50 configuration changes within a single hour (e.g., 15:00:00 to 15:59:59) within the file, the file is "evil" (a flood attack).

### Training Data
You have been provided with two corpora to test your script:
- `/app/corpora/clean/`: Contains 50 known-good log files.
- `/app/corpora/evil/`: Contains 50 known-bad log files (either containing malicious payloads or flood attacks).

Ensure your script handles character encodings and aggregations strictly using standard Linux utilities (bash, awk, grep, base64, iconv, date, etc.). Python, Perl, or other interpreters are strictly forbidden.

Write your complete solution to `/home/user/classifier.sh` and make it executable.