You are a support engineer investigating a recent crash of our multithreaded server application. To help the development team fix the issue, you need to collect specific diagnostic information from the system and summarize it in a report.

Please perform the following steps:

1. **Git History Forensics**: The server interacts with a database, and we suspect a legacy database password was accidentally committed and later removed from the repository located at `/home/user/server_repo`. The password was originally stored in a file named `db_config.json` under the JSON key `"db_pass"`. Find the original plaintext password.
2. **Crash Log Analysis**: The server generated a stack trace dump right before it crashed, which is saved at `/home/user/crash_trace.log`. Find the exact memory address where the segmentation fault occurred (look for the line indicating a Segfault).

Once you have gathered this information, create a diagnostic report at `/home/user/diagnostics.txt` with exactly the following format:

```text
PASSWORD: <the_found_password>
SEGFAULT_ADDR: <the_memory_address>
```

Make sure the file `/home/user/diagnostics.txt` contains only these two lines in the exact format specified.