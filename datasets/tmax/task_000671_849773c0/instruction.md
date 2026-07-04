You are a security researcher investigating a suspicious Python-based exfiltration tool found on a compromised Linux machine. The malware author left behind fragments of the tool's source code and some corrupted data. Your objective is to reverse-engineer the tool's key generation, recover a lost secret, salvage corrupted database logs, and produce a final analysis report.

Perform the following tasks:

1. **Git Forensics**: The malware author left a Git repository at `/home/user/malware_repo`. The repository contains the source code for the tool. At some point, the author committed a hardcoded secret salt, but later removed it to cover their tracks. Inspect the Git history to recover the value of the `SALT` string.

2. **Floating-Point Precision Repair**: The repository contains a script named `key_gen.py`. This script implements a chaotic logistic map to generate a numeric decryption key. However, the current implementation uses standard Python floats, which introduces precision errors after multiple iterations. 
   - You must modify or rewrite the logic to use Python's built-in `decimal` module.
   - Set the decimal context precision to exactly `50` (`decimal.getcontext().prec = 50`).
   - Use the recovered `SALT` string to initialize the generator (the script currently has a placeholder).
   - Run the map for exactly 100 iterations. The final generated value is the required decryption key.

3. **Database WAL Recovery**: The malware logged its targets to an SQLite database located at `/home/user/target_data/targets.db`. In an attempt to wipe the evidence, the malware executed a `DELETE` operation and zeroed out most of the main database file. However, the Write-Ahead Log (`targets.db-wal`) is still intact and contains the exfiltrated VIP target's email address. Extract this email address. 

4. **Reporting**: Compile your findings into a JSON file located at `/home/user/analysis_report.json`. The file must have the following exact structure:
```json
{
  "recovered_salt": "...",
  "precise_key": "...",
  "target_email": "..."
}
```
*Note: The `precise_key` should be represented as a string containing the exact decimal output after 100 iterations (e.g., "0.123456789...").*