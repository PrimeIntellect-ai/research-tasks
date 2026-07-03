You are a DevSecOps engineer tasked with analyzing a custom pre-authentication SSH greeter utility, demonstrating its vulnerabilities to stakeholders, and enforcing secure SSH configurations via "Policy as Code".

The system contains a vulnerable C program located at `/home/user/greeter`, with its source code available at `/home/user/src/greeter.c`. Additionally, an insecure SSH configuration file is located at `/home/user/sshd_config`.

You must complete the following objectives:

**1. Vulnerability Analysis & ELF Auditing**
Analyze `/home/user/src/greeter.c` and the compiled binary `/home/user/greeter`. Identify the primary Common Weakness Enumeration (CWE) identifier that leads to the buffer overflow vulnerability. 
Write the precise CWE ID (e.g., `CWE-123`) to a file named `/home/user/cwe.txt`.

**2. Exploit Crafting**
Demonstrate the vulnerability by writing a Python 3 script at `/home/user/exploit.py`. The script must output a raw binary payload to `stdout` such that when piped into the binary (i.e., `python3 /home/user/exploit.py | /home/user/greeter`), it triggers a return-to-text exploit, successfully altering the execution flow to execute the hidden `admin_shell` function. 
A successful exploit will cause the binary to print exactly `POLICY_BYPASS_SUCCESS`.

**3. SSH Hardening & Policy as Code**
The provided SSH configuration at `/home/user/sshd_config` is insecure.
First, create a hardened version of this file at `/home/user/sshd_config.fixed`. Ensure that the following three directives are explicitly set and uncommented:
- `PermitRootLogin no`
- `PasswordAuthentication no`
- `Protocol 2`

Next, implement a "Policy as Code" enforcement tool. Write a Python script at `/home/user/policy.py` that accepts a single command-line argument: the path to an `sshd_config` file.
Your script must parse the file and enforce the above three rules. 
- If all three directives are strictly enforced (set to the exact values above and uncommented), the script must print `PASS` to `stdout` and exit with code `0`.
- If any directive is missing, commented out, or set to a different value, the script must print `FAIL` to `stdout` and exit with code `1`.

Make sure your `policy.py` works dynamically and doesn't just hardcode checks for specific file paths. Automated tests will run your exploit and policy scripts to verify success.