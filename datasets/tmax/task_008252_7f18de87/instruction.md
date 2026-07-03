You are a security researcher analyzing a suspicious memory dump from a compromised machine. 

We have recovered a raw memory dump file located at `/home/user/dump.bin` and a partially written parsing script at `/home/user/extractor.py`. The parsing script was designed to extract candidate Command and Control (C2) domains or payload strings from the dump.

However, the memory dump contains corrupted segments (possibly an anti-forensic technique or simply memory corruption). When you run `/home/user/extractor.py dump.bin`, it crashes.

Your tasks are:
1. **Debug and fix `/home/user/extractor.py`**: Modify the script so it gracefully handles corrupted chunk sizes (e.g., sizes that would read past the end of the file) and truncated chunk headers. It should skip invalid chunks or break out of the loop safely without crashing, ensuring all valid chunks *before* and *after* the corruption are still processed and extracted.
2. **Extract candidates**: Run the fixed script to generate `/home/user/candidates.txt`. Each line in this file will contain an extracted string.
3. **Statistical Anomaly Investigation**: The true C2 payload is obfuscated and stands out statistically. Write a Python script (e.g., `/home/user/analyze.py`) that calculates the Shannon entropy of each string in `/home/user/candidates.txt`.
4. **Identify the payload**: Find the single string from the candidates that has the **highest Shannon entropy**. 
5. **Save the result**: Write this highest-entropy string exactly as it appears (no trailing newlines if not present in the string itself, though standard echo is fine) into `/home/user/flag.txt`.

Verify your work by ensuring `/home/user/flag.txt` contains exactly one line with the anomalous string.