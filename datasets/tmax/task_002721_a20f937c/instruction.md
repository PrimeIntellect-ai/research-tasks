You are a forensics analyst investigating a compromised Linux host. The attacker used a custom log obfuscation technique to hide their command-and-control (C2) activity within standard web access logs. We have recovered a collection of these logs, as well as a modified encryption library left behind by the attacker.

Your objectives:
1. **Fix the Vendored Package**: The attacker relied on a vendored copy of the `pyaes` Python library located at `/app/pyaes-1.6.1/`. They introduced a deliberate perturbation in `/app/pyaes-1.6.1/pyaes/aes.py` to break standard decryption for investigators (a syntax error or altered bitwise operation near the `SubBytes` step). You must identify and fix this perturbation so the package functions correctly.
2. **Reverse Engineer the Obfuscation**: The attacker's C2 logs contain hexadecimal strings in the User-Agent field. These strings are AES-encrypted using the fixed `pyaes` library. The AES key is hardcoded as `ForensicsTaskKey123!` (16 bytes). 
3. **Build an Adversarial Classifier**: We have provided two directories of extracted log entries:
   - `/app/corpora/clean/`: Contains normal, benign web requests.
   - `/app/corpora/evil/`: Contains malicious C2 requests.
   You must write a Python script at `/home/user/detector.py` that takes a single file path as a command-line argument. The script should read the log file, extract the hex-encoded User-Agent string, decrypt it using the fixed `pyaes` package (using ECB mode), and check for malicious payloads (e.g., command injection, SQLi, or known C2 commands). 
   - If the decrypted payload indicates malicious activity, print exactly `EVIL` to standard output.
   - If the log is benign (or decryption fails/yields normal browser agents), print exactly `SAFE`.

Requirements:
- Your `detector.py` must correctly classify 100% of the files in the `clean` corpus as `SAFE` and 100% of the files in the `evil` corpus as `EVIL`.
- The script must use the local vendored `pyaes` package at `/app/pyaes-1.6.1/`, not the system installed version (make sure to set your `PYTHONPATH` or `sys.path` appropriately).
- Be sure to handle potential padding properly after decryption.

Write the code, fix the package, and test it against the corpora. Once `detector.py` accurately flags all files, you are done.