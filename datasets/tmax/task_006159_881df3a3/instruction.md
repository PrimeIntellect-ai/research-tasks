You are an incident responder investigating a compromised web server. You have recovered two artifacts from the server:
1. A compiled Linux executable located at `/home/user/legacy_auth`. This binary was used to authenticate a highly privileged local service. It contains a hardcoded credential check, but the original source code for it is lost.
2. A source code snippet from the web application's login flow, saved at `/home/user/login.cpp`. The security team suspects this snippet contains a vulnerability that was used in a recent phishing campaign to redirect users to malicious domains after successful logins.

Your objectives are:
1. **Reverse Engineering & Cracking:** Analyze the `/home/user/legacy_auth` executable to understand its custom password validation logic. Then, write a C++ program named `/home/user/crack.cpp` that programmatically recovers or brute-forces the hardcoded 5-character lowercase password. Compile and run your C++ program to find the password.
2. **Code Auditing & CWE Identification:** Analyze the `/home/user/login.cpp` file. Identify the specific Common Weakness Enumeration (CWE) identifier for the vulnerability present in the snippet.

Once you have completed your analysis, create a report file at `/home/user/findings.txt` with exactly two lines:
- Line 1: The recovered 5-character password.
- Line 2: The standard CWE identifier for the vulnerability in `login.cpp` (format: `CWE-XXX`).

Do not include any extra text, spaces, or formatting in `findings.txt` other than the requested values on their respective lines.