You are a security researcher analyzing a suspicious stripped binary found on a compromised data processing server. The binary is located at `/app/malware_encoder`. It appears to be transforming floating-point sensor data before exfiltration, but its exact mechanism is unknown.

The threat actors attempted to cover their tracks by deleting the source code and obfuscating the binary. However, a heavily mangled local Git repository remains at `/home/user/suspicious_repo`. 

Your objectives:
1. **Forensic Recovery**: Inspect the Git history in `/home/user/suspicious_repo`. The threat actors accidentally committed an intermediate state trace log and a configuration secret before deleting them. Recover the secret float constant.
2. **Precision Loss Tracking**: Analyze the intermediate trace log and the binary's behavior. The binary performs a mathematical transformation on standard input (reading one float per line). It involves the secret constant and introduces a specific type of precision loss (truncation or rounding at an intermediate step).
3. **Reconstruction**: Write a Python 3 script at `/home/user/reconstructed_encoder.py` that behaves identically to the stripped binary. It must read a sequence of floats from `stdin` (one per line) and print the encoded output to `stdout` (one per line), matching the binary's output bit-for-bit.

Your reconstructed script will be rigorously tested against the original binary using a fuzzing verifier. It must handle any float between -1000.0 and 1000.0 exactly as the malware does.