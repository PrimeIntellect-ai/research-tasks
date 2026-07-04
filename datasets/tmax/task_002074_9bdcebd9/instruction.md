We have a critical issue with our custom log aggregation systemd service (`log-validator.service`). It continuously fails to start because the underlying validation binary crashes when encountering specific malformed log entries from our upstream nodes.

Your objective is to diagnose the crash condition and create a pre-processor script to sanitize the input logs before they reach the binary.

System details and resources:
- The crashing binary is located at `/app/log_validator`. It is a stripped binary that reads log lines from `stdin`.
- We have isolated a set of logs that cause the service to crash in `/app/corpus/evil/`.
- We also have a set of perfectly valid logs that must remain unmodified in `/app/corpus/clean/`.
- Both corpora consist of plain text log files.

Task:
Write a filter script at `/home/user/filter_wrapper.py` (you can use Python, Perl, or Ruby, but ensure it's executable and has the correct shebang). The script must read lines from standard input (`stdin`), filter out or sanitize ONLY the specific lines that cause `/app/log_validator` to crash, and print the safe lines to standard output (`stdout`). 

Constraints:
1. You must not modify the `/app/log_validator` binary.
2. 100% of the lines that cause crashes (as found in the evil corpus) must be removed or neutralized.
3. 100% of the normal log entries (as found in the clean corpus) must be preserved exactly as they are.
4. Your script will be tested automatically by piping files into it. Do not add interactive prompts.