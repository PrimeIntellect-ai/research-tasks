You are an operations engineer triaging a critical incident for an internal packet processing service called `netdaemon`. 

Recently, the service started experiencing two major issues:
1. It intermittently hangs and spikes CPU to 100%.
2. The internal statistics for `total_bytes_processed` are inconsistent under high load.

The code is located in `/home/user/netdaemon/`. It is a C project managed with Git. 

Your tasks are as follows:
1. **Regression Identification:** Use `git bisect` to identify the exact commit hash that introduced the hanging behavior. Write the full, 40-character commit hash to `/home/user/bad_commit.txt`. A test script `test_hang.sh` is provided in the repository to check if a commit hangs.
2. **Root Cause Analysis & Fix (Recursion):** Analyze the provided `/home/user/traffic.pcap` to understand what kind of packet is triggering the hang. The issue lies in the recursive TLV (Type-Length-Value) parsing function in `parser.c`. Fix the code so it properly rejects malformed packets (e.g., zero-length or infinite loops) without hanging. 
3. **Root Cause Analysis & Fix (Race Condition):** The daemon uses a multi-threaded worker pool (`worker.c`) to process packets. Fix the race condition that causes `total_bytes_processed` to be calculated incorrectly. You must use standard pthread mutexes to protect the shared state.
4. **Validation:** Ensure the code compiles cleanly by running `make` in `/home/user/netdaemon/`. 
5. **Execution:** Run the fixed daemon against the provided pcap file: `./netdaemon /home/user/traffic.pcap > /home/user/final_output.txt`.

Constraints:
- Do not modify the `Makefile`.
- The daemon must exit cleanly and output the correct final statistics to `/home/user/final_output.txt`.
- Do not hardcode the final answer; your code must dynamically process the pcap file.