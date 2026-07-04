You are a DevSecOps engineer tasked with enforcing security policies on a legacy C++ web backend component. You must perform a code audit, conduct a basic cryptanalysis on a custom cryptographic primitive, and implement a data redaction utility.

You have been provided with the following files:
1. `/home/user/auth_service.cpp`: The source code for the legacy web authentication service.
2. `/home/user/sbox.txt`: A text file containing a 4-bit S-box (16 space-separated integers from 0 to 15) used in the service's custom session token generation algorithm.
3. `/home/user/requests.log`: A log file containing raw HTTP request headers and payloads.

Perform the following three tasks:

**Task 1: Vulnerability Identification (CWE)**
Audit `/home/user/auth_service.cpp`. There is a prominent vulnerability in the `parse_http_header` function where an untrusted input is copied into a fixed-size buffer without length checking. 
Identify the most specific CWE identifier for this vulnerability. 
Write ONLY the CWE identifier (format: `CWE-XXX`) to a new file at `/home/user/cwe_finding.txt`.

**Task 2: Differential Cryptanalysis (DDT)**
The service uses a custom substitution network for token generation, relying on the 4-bit S-box provided in `/home/user/sbox.txt`. To prove this is weak policy, you must find the maximum differential probability for this S-box.
Compute the Difference Distribution Table (DDT) for the S-box. Find the input difference (`DeltaIn`) and output difference (`DeltaOut`) that yield the highest occurrence count, excluding the trivial case where `DeltaIn = 0` and `DeltaOut = 0`.
If there is a tie, choose the one with the smallest `DeltaIn` value.
Write the result to `/home/user/ddt_max.txt` in the exact format: `DeltaIn,DeltaOut,Count` (use decimal integers for all three values).

**Task 3: Sensitive Data Redaction**
The `/home/user/requests.log` file inadvertently records sensitive user data. 
Write a C++ program at `/home/user/redact.cpp` that reads `/home/user/requests.log` and replaces any 16-digit credit card number (exactly 16 consecutive digits, e.g., `1234567890123456`) with the exact string `[REDACTED]`.
Compile your program and execute it such that it writes the cleaned log to `/home/user/clean_requests.log`.

Ensure all output files are placed exactly as requested.