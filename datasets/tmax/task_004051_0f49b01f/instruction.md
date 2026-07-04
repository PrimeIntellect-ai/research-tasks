You are a forensics analyst investigating a compromised Linux host. The incident response team has isolated a directory containing suspicious files dropped by the attacker, and they suspect the attacker attempted to establish persistence via privilege escalation backdoors and modified file permissions.

Your objective is to write and execute a Python script that audits this directory, verifies cryptographic hashes against a list of Known Bad Indicators of Compromise (IOCs), and extracts embedded evidence flags.

**Environment Setup & Inputs:**
- The suspicious files are located in `/home/user/suspect_dir` (and its subdirectories).
- A list of known malicious SHA-256 hashes is located at `/home/user/ioc_hashes.txt` (one hex string per line).

**Requirements for your Python script:**
1. **Permission Audit:** Recursively scan `/home/user/suspect_dir`. Identify any files that are:
   - World-writable (others have write permission).
   - SUID or SGID (Set-User-ID or Set-Group-ID bit is set).
2. **Cryptographic Verification:** Compute the SHA-256 hash of *every* file in the directory tree. Compare the computed hash against the hashes provided in `/home/user/ioc_hashes.txt`.
3. **Evidence Extraction:** If a file is flagged as SUID, SGID, *or* matches an IOC hash, you must read its contents and extract any strings matching the exact regular expression: `EVIDENCE_FLAG_[A-Z0-9]{16}`.
4. **Reporting:** Generate a final JSON report at `/home/user/forensics_report.json` with the exact following structure (lists should contain absolute file paths, and flags should be unique):

```json
{
  "world_writable_files": [
    "/home/user/suspect_dir/example_writable.sh"
  ],
  "suid_sgid_files": [
    "/home/user/suspect_dir/example_suid.bin"
  ],
  "ioc_matches": [
    "/home/user/suspect_dir/example_malware.elf"
  ],
  "extracted_flags": [
    "EVIDENCE_FLAG_A1B2C3D4E5F6G7H8"
  ]
}
```

*Note: Lists can be empty if no files match the criteria. Sort the absolute paths in the lists alphabetically to ensure consistent reporting. Sort the extracted flags alphabetically as well.*

Write the script, execute it to generate the report, and ensure the resulting `/home/user/forensics_report.json` is perfectly formatted and accurate.