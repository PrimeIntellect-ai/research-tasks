You are an operations engineer triaging an incident. A scheduled log processing pipeline has stalled, causing alerts to fire. 

The pipeline relies on a Bash script located at `/home/user/parse_pcap.sh`. This script parses a simplified network packet capture log located at `/home/user/traffic.log` to calculate the total payload size of the captured traffic. 

Currently, running `./parse_pcap.sh traffic.log` hangs indefinitely and never completes. Additionally, a previous engineer noted that even when the script doesn't hang, it sometimes crashes at the very end of the file with a syntax error related to mathematical evaluation.

Your tasks are:
1. **Delta Debugging / Minimization:** Determine the exact line number (1-indexed) in `/home/user/traffic.log` that triggers the infinite loop. Write this line number (just the integer) to `/home/user/bug_line.txt`.
2. **Bug Fixing:** Inspect `/home/user/parse_pcap.sh`. Fix the infinite loop issue (loop termination repair) and the crash at the end of the file (boundary condition/off-by-one repair). 
3. **Save Fixed Code:** Save the corrected Bash script to `/home/user/parse_pcap_fixed.sh` and ensure it is executable.
4. **Execution:** Run your fixed script on `/home/user/traffic.log`. Write the resulting total payload size (just the integer) to `/home/user/total_bytes.txt`.

Ensure all output files are placed exactly in `/home/user/` with the specified names. You must use Bash to solve this; do not rewrite the parsing logic in Python, awk, or other languages (though standard CLI tools like `grep`, `head`, etc., are permitted for your own investigation).