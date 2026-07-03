You are a DevOps engineer investigating a recent severe outage on your company's payment gateway. 

You have been provided with a directory `/home/user/forensics/` containing two files:
1. `server.log`: The application log file. Unfortunately, a failing disk controller corrupted parts of the log. It contains null bytes (`\x00`) and invalid UTF-8 sequences scattered throughout, particularly around the timestamps and IP addresses.
2. `traffic.pcap`: A network packet capture of the HTTP traffic going to the server during the incident window.

Your objective is to:
1. Parse and clean the corrupted `server.log` to locate the single `[CRITICAL]` error event ("Payment Gateway Crash").
2. Reconstruct the log entry to identify the exact source IP address that triggered the crash.
3. Analyze the `traffic.pcap` file to find the HTTP GET request sent by that specific IP address just before the crash (the timestamps in the log and the pcap match perfectly).
4. Extract the full requested URI (the path and query string, e.g., `/?checkout=true&id=malicious...`) of that specific malicious packet.
5. Write ONLY the exact, full URI string to `/home/user/payload.txt`.

You may write Python scripts to accomplish this. Standard packet analysis tools like `tcpdump` are available, or you can install Python libraries like `scapy` or `dpkt` using pip if needed.