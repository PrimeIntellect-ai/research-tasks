You are a DevSecOps engineer tasked with enforcing security policies and identifying a recent breach. We suspect an attacker has bypassed our legacy authentication gateway by forging access tokens.

You have been provided with an access log at `/home/user/gateway.log`.

**Legacy Token Mechanism:**
After interviewing the developers of the legacy system, you learned the following about how tokens were generated:
1. The plaintext payload of the token is constructed exactly as: `<Timestamp>:<UserID>` (e.g., `2024-10-12T08:15:30Z:alice`).
2. This plaintext is XORed with a static, repeating Secret Key.
3. The resulting byte array is Base64 encoded to form the final `Token`.

**Your Objective:**
1. **Cryptanalysis & Protocol Reverse Engineering:** Since the Secret Key was lost, you must perform a known-plaintext attack to recover the static XOR Secret Key. Most of the traffic in the log is legitimate, meaning the same key is used repeatedly.
2. **Log Parsing & Token Validation:** Once you have recovered the primary Secret Key, parse `/home/user/gateway.log` and validate the token for every request. Reconstruct the expected token for each log line using the recovered key and compare it to the token provided in the log.
3. **Attacker Identification:** Identify all requests where the provided token is invalid (i.e., it does not match the expected token constructed with the recovered primary Secret Key). 

Extract the IP addresses of the forged/invalid requests.
Write the malicious IP addresses to `/home/user/malicious_ips.txt`, with one IP address per line, sorted in ascending order, with strictly unique entries. 

You may use any programming language or shell tools available on the system to complete this task.