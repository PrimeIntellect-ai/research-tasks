You are a DevSecOps engineer responsible for enforcing security policy as code. You have been assigned to audit a legacy C++ authentication component that has been flagged for potentially allowing privilege escalation and using weak custom cryptography.

In `/home/user/auth_policy.cpp`, there is a C++ module that processes incoming authentication payloads. 
A suspicious, encoded binary payload has been captured and saved to `/home/user/payload.bin`.

Your task is to:
1. Audit `/home/user/auth_policy.cpp` to understand the custom decoding algorithm.
2. Decode the contents of `/home/user/payload.bin`. You may write and run a C++ script to accomplish this.
3. Identify the CWE (Common Weakness Enumeration) identifier for the primary memory safety vulnerability in `process_auth` that allows an oversized decoded payload to overwrite adjacent memory (which could lead to privilege escalation).
4. Identify the CWE identifier for the use of a custom, weak encoding mechanism instead of standard cryptography.
5. Generate a DevSecOps policy violation report at `/home/user/policy_report.json` with the following exact keys and format:

```json
{
  "weak_crypto_cwe": "CWE-XXX",
  "buffer_overflow_cwe": "CWE-YYY",
  "decoded_payload": "<the exact decoded ASCII string from payload.bin>"
}
```

(Replace XXX and YYY with the correct numbers, e.g., CWE-120, CWE-327, etc.)