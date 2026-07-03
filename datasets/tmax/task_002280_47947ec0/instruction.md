You are a DevOps engineer tasked with debugging a log anomaly detection system. 

We have a proprietary log format that encrypts log entries. A stripped binary tool is provided at `/app/log_decryptor` which takes a log file path as an argument and outputs the decrypted log lines to standard output.

We have a Bash script at `/home/user/detector.sh` that is supposed to analyze a given raw log file and detect "timeline sequence anomalies" across multiple microservices. 
A standard transaction flows from `[ServiceA]` -> `[ServiceB]` -> `[ServiceC]`. The timestamps must be strictly non-decreasing (i.e., Time(A) <= Time(B) <= Time(C)). If any transaction in the log violates this chronological order, the log file is considered anomalous ("evil") and the script should exit with a non-zero status. If all transactions follow the correct order, it should exit with 0 ("clean").

Unfortunately, the current `detector.sh` is failing to detect anomalies and constantly returns 0. It contains several Bash-specific bugs:
1. A scoping issue related to how data is read and variables are populated.
2. A logic/formula flaw in how timestamps are compared.
3. Potential issues with loop control and exiting.

Your task:
1. Reverse-engineer the behavior of `/app/log_decryptor` if needed, or simply use it as an oracle to read the files.
2. Fix the bugs in `/home/user/detector.sh`.
3. Ensure `/home/user/detector.sh <filepath>` correctly exits with `0` for normal logs and `1` (or any non-zero) for anomalous logs.

You can test your script against the corpora located at `/app/corpus/clean/` and `/app/corpus/evil/`. Every file in the clean directory must result in an exit code of `0`, and every file in the evil directory must result in a non-zero exit code.