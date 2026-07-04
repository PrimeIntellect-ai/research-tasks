You are a DevOps engineer investigating a series of crashes in a custom log aggregation service. 

We have a proprietary log ingestion binary located at `/app/log_ingester`. Recently, it has been crashing sporadically. The binary is stripped, and we don't have the source code. 

To help you investigate, we have captured a core dump from one of the crashes at `/app/crash.core`, along with a packet capture of the incoming syslog traffic at `/app/traffic.pcap` leading up to the crash.

Your task is to:
1. Analyze the provided pcap file and core dump to understand the root cause of the crashes in `/app/log_ingester`. You may use tools like `gdb` and `tshark`/`tcpdump`.
2. Write a C++ program at `/home/user/sanitiser.cpp` and compile it to an executable at `/home/user/sanitiser`.
3. The `/home/user/sanitiser` executable must act as a standard-in to standard-out filter. It should read log lines one by one.
4. If a log line contains the malformed pattern/payload that triggers the crash in `/app/log_ingester`, your sanitiser MUST drop the line (print nothing for that line).
5. If a log line is benign, your sanitiser MUST print it to stdout exactly as it was received, including the trailing newline.

The automated verification system will test your `/home/user/sanitiser` binary against two hidden corpora of log lines:
- A "clean" corpus of valid logs. Your sanitiser must output these 100% unchanged.
- An "evil" corpus of malicious/crashing logs. Your sanitiser must drop 100% of these.

Ensure your code handles typical standard input reading robustly and efficiently. Make sure the compiled binary `/home/user/sanitiser` is executable.