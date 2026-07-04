You are a DevSecOps engineer tasked with enforcing policy as code for a legacy system. 

We have a legacy CGI web application binary located at `/app/legacy_cgi`. The source code was lost, and the binary is stripped. It processes incoming HTTP requests, but we suspect it has critical vulnerabilities (such as command injection or directory traversal) based on how it handles the `target=` parameter in the query string or body.

Your goal is to write a set of Bash scripts to secure the system against these threats, apply network policies, and harden our SSH configuration.

**Phase 1: Web Application Firewall (WAF) Filter**
1. Analyze `/app/legacy_cgi` using tools like `strings`, `objdump`, or `strace` (or by treating it as a black-box oracle and fuzzing it) to identify the exact syntax of the payloads that exploit it.
2. Write a Bash script at `/home/user/waf_filter.sh` that takes a single argument: the path to a file containing a raw HTTP request.
3. The script must analyze the request and:
   - Print exactly `CLEAN` to stdout and exit with status code `0` if the request is benign.
   - Print exactly `EVIL` to stdout and exit with status code `1` if the request contains an exploit payload targeting `/app/legacy_cgi`.
   - Your filter must be precise: it should block malicious metacharacters or traversal sequences without blocking legitimate alphanumeric input.

**Phase 2: Network Policy Enforcement**
Write a script at `/home/user/network_harden.sh` that uses `iptables` commands to block all incoming TCP traffic on port `8080` (where the legacy server used to run) while explicitly allowing port `443`. The script must run without errors.

**Phase 3: SSH Hardening**
We need to enforce strict key management. Write a script at `/home/user/ssh_harden.sh` that reads `/home/user/.ssh/authorized_keys`, removes any public keys using deprecated, weak algorithms (`ssh-rsa` and `ssh-dss`), and writes the cleaned output back to `/home/user/.ssh/authorized_keys`. It must verify the file integrity by generating a SHA256 checksum of the new file and storing it in `/home/user/.ssh/authorized_keys.sha256`.

Ensure all scripts are executable. Do not attempt to run the iptables script if it requires root in your current environment; just write the correct commands into the file.