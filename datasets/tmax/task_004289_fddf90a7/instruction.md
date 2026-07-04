You are acting as a penetration tester and security analyst evaluating a set of file upload logs from a compromised server. The server's upload handler was suspected of being vulnerable to path traversal attacks.

The server logs are located at `/home/user/upload_logs.txt`. 
Each line in the log file follows this format:
`[Timestamp] | [IP Address] | [MD5_Auth_Hash] | [Base58_Encoded_Filename_Payload]`

To analyze these logs, you need to decode the filenames. The system administrators used a specific Python package for base58 encoding. The source code of this package is vendored at `/app/base58-2.1.1`. 

However, the threat actor subtly sabotaged the vendored base58 package before the logs were fully captured. Specifically, the standard Bitcoin alphabet string inside the package has been perturbed (two characters were swapped). 
Your tasks are:
1. Identify the sabotage in the vendored `/app/base58-2.1.1` package and fix it so that it uses the standard Bitcoin base58 alphabet (`123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz`).
2. Use the fixed package to decode the `Base58_Encoded_Filename_Payload` from each log entry.
3. Perform intrusion detection by scanning the decoded payloads for path traversal patterns (e.g., strings containing `../`, `..\`, or URL-encoded equivalents like `..%2f`).
4. For every log entry that contains a path traversal payload, crack the `MD5_Auth_Hash`. The passwords are known to be strictly 4-digit PINs (from `0000` to `9999`).
5. Write your final findings to `/home/user/suspects.txt`. Each line must correspond to a malicious entry, formatted exactly as:
`IP_Address,Cracked_PIN,Decoded_Payload`

Your final solution will be evaluated based on the F1-score of correctly identified malicious IP addresses and the accuracy of the cracked PINs and decoded payloads. You do not need to output benign log entries.