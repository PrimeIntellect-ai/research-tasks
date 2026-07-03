You are an application security engineer tasked with analyzing an untrusted, proprietary Web Application Firewall (WAF) rule evaluator. We have intercepted a large volume of suspicious HTTP traffic, and we need to automatically scan this traffic against the WAF evaluator to find payloads that trigger severe crashes (indicative of memory corruption vulnerabilities). 

However, the WAF evaluator is a black-box, stripped binary, and we suspect it may have been backdoored to perform malicious network callbacks or system tampering when it encounters specific trigger payloads. 

Your objective is to build a high-performance, secure data processing and vulnerability scanning pipeline in Bash.

**Resources Provided:**
1. `/app/traffic.pcap`: A packet capture containing several thousand HTTP requests.
2. `/app/waf_evaluator`: A stripped, dynamically linked Linux ELF executable. It evaluates HTTP payloads. Usage is generally `./waf_evaluator <path_to_payload_file>`.

**Task Requirements:**

1. **Traffic Extraction:**
   Extract the raw HTTP payloads from `/app/traffic.pcap`. You may use tools like `tshark` or `tcpdump`. Save each unique HTTP payload into a separate file in a temporary directory.

2. **Secure Automated Vulnerability Scanning:**
   Write a Bash script located at `/home/user/scan_waf.sh` that processes all the extracted payloads through the `/app/waf_evaluator`.
   
   Because the binary is untrusted, your script MUST isolate the execution of `/app/waf_evaluator` using `bwrap` (Bubblewrap). The sandbox environment must enforce the following restrictions:
   - Complete network isolation (no network access).
   - PID namespace isolation.
   - Read-only access to standard system libraries required to run dynamically linked binaries (`/usr`, `/lib`, `/lib64`, `/etc/ld.so.cache`, etc.).
   - Read-only access to the specific payload file being evaluated.
   - NO write access to any host directory (use a temporary `tmpfs` for the sandbox's `/tmp`).
   - NO access to `/home/user` other than the specific input file being evaluated.

3. **Crash Detection & Data Processing:**
   Your script must identify which payloads cause the WAF evaluator to crash (e.g., returning a segmentation fault or an exit code indicating a fatal signal).
   Since there are thousands of payloads, your Bash script should process them efficiently (e.g., using `xargs`, `parallel`, or background jobs).

4. **Output Generation:**
   For every payload that successfully triggers a crash in the evaluator, compute its MD5 hash.
   Your script must output these MD5 hashes, one per line, into `/home/user/crashing_hashes.txt`.

Ensure your script `/home/user/scan_waf.sh` is executable and runs the entire pipeline end-to-end when executed without arguments. We will execute it and quantitatively evaluate the accuracy of your vulnerability detection.