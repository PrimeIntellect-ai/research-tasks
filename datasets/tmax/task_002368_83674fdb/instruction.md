You are a compliance analyst tasked with generating audit trails for a legacy network appliance. We are replacing this appliance, but compliance rules require us to maintain its exact proprietary "SecureAudit" packet logging format and inline firewall behavior.

You have been provided with a video recording of the legacy system's diagnostic feed at `/app/traffic_monitor.mp4`. The video itself shows a scrolling matrix, but the developers left an embedded subtitle track (accessible via `ffmpeg`) that logs several exact plaintext payloads and their corresponding firewall actions or 8-bit hex hashes.

Your objective:
1. Extract the subtitle track from the video to recover the training pairs (payloads and their corresponding outputs).
2. Perform cryptanalysis to deduce the logic of the "SecureAudit" hashing algorithm. We know it processes the string sequentially, updating an 8-bit state character-by-character using basic bitwise/arithmetic operations (XOR, addition, subtraction). 
3. Deduce the legacy inline firewall rules (which flag specific malicious strings associated with CWEs and drop traffic) based on the special cases in the subtitle logs.
4. Implement a pure Bash script at `/home/user/audit_hash.sh` that perfectly replicates this entire logic.

Script Requirements:
- It must accept exactly one argument: the payload string.
- If the payload triggers a firewall rule, print the exact action keyword (e.g., "DENY" or "ALERT") and exit with the corresponding non-zero exit code as implied by the system's behavior (you'll need to deduce this if standard, or use exit 1 for DENY and exit 2 for ALERT).
- Otherwise, print the computed 8-bit hash formatted as `0xXX` (e.g., `0x55`, `0x0f`) and exit with 0.
- Ensure the script is executable (`chmod +x`).

The automated verification system will extensively fuzz your script against a hidden reference binary using thousands of random strings. Your script's output and exit codes must be BIT-EXACT equivalent to the reference implementation for all possible inputs.