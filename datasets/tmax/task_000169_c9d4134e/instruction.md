You are a Site Reliability Engineer responding to a sudden service outage. A critical Go microservice just crashed, causing a spike in downtime.

You have been provided with two pieces of evidence:
1. A raw memory dump of the crashed Go process, located at `/home/user/crash-dump.bin`.
2. The Git repository of the microservice, located at `/home/user/app-repo`.

Your task is to identify the root cause of the crash and pinpoint exactly when it was introduced into the codebase.

Instructions:
1. Analyze the raw memory dump `/home/user/crash-dump.bin` to find the exact panic message. The application was programmed to prefix custom fatal errors with `panic: SRE_CRITICAL_ERR: `. Extract this full line.
2. Search the Git history in `/home/user/app-repo` to find the commit hash that *first* introduced this exact error string in the code.
3. Write your findings to a file named `/home/user/report.txt` in the following exact format:

```
COMMIT_HASH:<full_40_character_commit_hash>
ERROR:<extracted_error_message_without_the_"panic: "_prefix>
```

Example of `/home/user/report.txt`:
```
COMMIT_HASH:1a2b3c4d5e6f7g8h9i0j1a2b3c4d5e6f7g8h9i0j
ERROR:SRE_CRITICAL_ERR: concurrent map writes in caching layer
```

Ensure the file `/home/user/report.txt` is created with the correct format before you finish.