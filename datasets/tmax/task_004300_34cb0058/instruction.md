You are a DevSecOps engineer responsible for enforcing infrastructure security policies as code. An air-gapped system has transmitted its latest security audit logs via an optical data diode. The transmission was captured as a video file located at `/app/audit_transmission.mp4`. 

Your objective is to extract the audit logs from this video, implement a high-performance policy evaluation engine in C, and accurately classify the system states to identify security vulnerabilities.

### Phase 1: Data Extraction
The video `/app/audit_transmission.mp4` contains a sequence of QR codes. Each QR code encodes a portion of a JSON array containing audit events.
1. Extract the frames from the video. 
2. Decode the QR codes (e.g., using `zbarimg`).
3. Reconstruct the decoded payload into a valid JSON file. This is your training/development dataset.

### Phase 2: Policy Engine Implementation
Write a C program at `/home/user/policy_enforcer.c` that parses an audit JSON file (provided as the first command-line argument) and evaluates three specific security policies.

Each JSON object in the array has the following structure:
```json
{
  "id": "evt_001",
  "file_owner": "root",
  "file_permissions": "4755",
  "cert_issuer": "CN=InternalCA",
  "cert_subject": "CN=InternalCA",
  "cert_in_trust_store": false,
  "user_input": "admin' OR 1=1--"
}
```

Implement the following DevSecOps policies. An event should be flagged as VULNERABLE (1) if it violates **any** of the following rules, otherwise SAFE (0):

**Rule 1: Privilege Escalation Auditing**
Flag if the `file_owner` is "root" AND the `file_permissions` indicate the SUID bit is set (the first digit of the 4-digit octal permission is 4 or 6). 

**Rule 2: Certificate Chain Validation**
Flag if the certificate is self-signed (i.e., `cert_issuer` exactly matches `cert_subject`) AND `cert_in_trust_store` is `false`.

**Rule 3: Injection Vulnerability Analysis**
Flag if the `user_input` string contains any of the following potentially malicious SQL/Command injection substrings:
- `' OR `
- `; DROP `
- `--`
- `UNION SELECT`

### Phase 3: Integration
Compile your C program to the executable `/home/user/policy_engine`. 
The program must output a CSV format strictly to `stdout` with the header `id,is_vulnerable`, followed by the evaluation of each event.

Example output:
```csv
id,is_vulnerable
evt_001,1
evt_002,0
```

Use your extracted dataset to test your implementation. When you are finished, we will run your `/home/user/policy_engine` binary against a hidden, held-out JSON test set (`/app/hidden_test_audit.json`) to evaluate its classification accuracy. 

You may install any necessary C libraries (e.g., `libcJSON-dev` or `libjansson-dev` for parsing) and video processing tools (e.g., `ffmpeg`, `zbar-tools`).