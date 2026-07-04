You are a DevOps engineer investigating a critical issue in a production environment. 

A background process called `traffic_sim.sh` is currently running on this system. It logs HTTP traffic data to a file originally located at `/home/user/service.log`. However, a junior developer accidentally ran `rm /home/user/service.log` earlier today. 

Since the `traffic_sim.sh` process was never restarted, it still holds an open file descriptor to the deleted log file, and is continuing to write to it. 

Recently, our monitoring systems alerted us to a statistical anomaly: a single request experienced a massive latency spike (over 8000 milliseconds) resulting in an HTTP 500 error.

Your task is to:
1. Locate the running `traffic_sim.sh` process.
2. Recover the contents of the deleted log file directly from the process's file descriptors.
3. Parse the recovered log data to find the single log entry that has a `status` of 500 and a `latency` greater than 8000.
4. Extract the IP address from that specific anomalous log entry.
5. Write ONLY the extracted IP address to `/home/user/culprit_ip.txt`.

The log entries are formatted as pseudo-JSON, but be aware that they might contain minor formatting edge-cases. 

Make sure `/home/user/culprit_ip.txt` contains exactly one line with just the IPv4 address.