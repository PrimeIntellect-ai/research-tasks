You are an operations engineer triaging an incident. A log processing script `/home/user/log_processor.py` occasionally deadlocks and hangs indefinitely when processing certain batches of log lines. 

Your objective is to:
1. Use test minimization / delta debugging techniques to isolate the exact single line from `/home/user/incoming_logs.txt` that triggers the deadlock. The script takes a file path as an argument (e.g., `python3 /home/user/log_processor.py <file>`).
2. Identify the specific system call that the deadlocked thread is stuck waiting on (you may use `strace` or inspect the script's behavior).

Once you have identified the failing log line and the system call, write your findings to a file named `/home/user/triage_report.txt` in the exact following format:

```
FAILING_LINE: <exact text of the log line that causes the hang>
SYSCALL: <name of the system call it hangs on>
```

For example:
```
FAILING_LINE: INFO: Connection closed by peer
SYSCALL: epoll_wait
```

Note: The script completes successfully (exit code 0) if no deadlock-triggering lines are present. When the deadlock occurs, the script hangs forever and must be killed.