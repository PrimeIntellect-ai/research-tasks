You are a backup administrator tasked with archiving application logs. Before archiving, we must ensure that no sensitive Personally Identifiable Information (PII) or malicious injection payloads are stored in our long-term storage.

You need to complete two main objectives:

**Objective 1: Fix the Archiving Tool**
We use a standard (vendored) lightweight shell-based archiving package called `bash-archive-tool` (version 1.0.0). Its source code is located at `/app/bash-archive-tool-1.0.0`. 
Recently, a junior administrator made a mistake and accidentally broke the tool's main script, preventing it from functioning correctly. 
1. Locate the perturbation in `/app/bash-archive-tool-1.0.0/archive.sh` and fix it so the package works normally again. 
2. Ensure the script is executable.

**Objective 2: Build a Log Classifier**
You must write a Bash script at `/home/user/classifier.sh` that detects whether a given log file is safe to archive or if it contains forbidden data.
Your script will be invoked as follows:
`/home/user/classifier.sh <path_to_log_file>`

The script must analyze the file and:
- Print exactly `CLEAN` to standard output and exit with status `0` if the file is safe.
- Print exactly `EVIL` to standard output and exit with status `1` if the file contains forbidden data.

Forbidden data is strictly defined as any file containing AT LEAST ONE line that matches either of these conditions:
1. Contains a 16-digit credit card number formatted exactly as `XXXX-XXXX-XXXX-XXXX` (where `X` is any digit 0-9).
2. Contains the exact string `[MALICIOUS_INJECTION]`.

To help you develop and test your script, we have provided two directories containing sample logs:
- `/app/corpus/clean/` : Contains logs that are completely safe. Your script MUST classify all of these as CLEAN.
- `/app/corpus/evil/` : Contains logs with hidden PII or malicious patterns. Your script MUST classify all of these as EVIL.

Ensure your script is robust, handles varying file sizes, and strictly follows the output and exit code requirements.