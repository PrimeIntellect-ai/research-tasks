As a DevOps engineer, you are investigating a recent production outage caused by our custom C-based log ingestion daemon. The daemon binary is located at `/app/log_ingest`. Unfortunately, it is a stripped binary without debug symbols. 

We suspect the crash is caused by a subtle timezone parsing bug when it processes malformed timestamps in the logs. 

I have provided two artifacts from the incident:
1. A core memory dump from the crash: `/home/user/crash.core`
2. The raw, 50MB log file from that hour: `/home/user/production.log`

Your task:
1. Analyze the core dump to extract the malformed timezone string that triggered the crash.
2. Use delta debugging/test minimization techniques on `production.log` to isolate the crashing log entry.
3. Determine the absolute *minimal* byte sequence required to trigger the crash in `/app/log_ingest`.
4. Write a C program at `/home/user/gen_repro.c`. When compiled and executed, this program must write your absolutely minimized crashing payload to a file named `/home/user/minimized_crash.log`.

The system will verify your solution programmatically. To succeed:
- `/app/log_ingest /home/user/minimized_crash.log` must result in a Segmentation Fault (SIGSEGV).
- The file size of `/home/user/minimized_crash.log` must be as small as possible. The automated metric will grade you based on the byte-size of this file. Smaller is better.