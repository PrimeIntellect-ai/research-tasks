You are a compliance analyst responsible for verifying the integrity and security of audit trails. We recently intercepted a batch of audit logs from a suspected compromised endpoint. These logs are stored in a proprietary binary format. 

You have been provided with the executable `/app/audit_compiler`, a stripped binary that the endpoint uses to package these audit files. It takes two arguments—a destination filename and the file content—and outputs the encoded payload to stdout. 

We have 500 such intercepted payload files in the directory `/home/user/audit_data/`. Some of these payloads are benign, but others are malicious attempts to exploit a path traversal vulnerability (CWE-22) in the log ingestion server. Furthermore, some files may be corrupted.

Your task is to:
1. Analyze the behavior of `/app/audit_compiler` (e.g., by observing its outputs) to reverse-engineer the proprietary file format, including its encoding scheme, integrity checksums, and structure.
2. Write a Python script at `/home/user/analyze.py` that reads all files in `/home/user/audit_data/`, decodes them, and verifies their integrity.
3. Identify which files are both valid (integrity checksum matches) AND malicious. A payload is malicious if its decoded target filename implies a path traversal (e.g., contains `../` or starts with an absolute path `/`).
4. Your script must generate a CSV report at `/home/user/report.csv` with exactly two columns: `filename` (the name of the file in `/home/user/audit_data/`, e.g., `log_0.bin`) and `is_malicious` (1 if valid and malicious, 0 otherwise).

Your final script will be evaluated based on the accuracy of `/home/user/report.csv` against a ground-truth label set. You must achieve an accuracy of at least 95%.