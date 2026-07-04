You are tasked with a vulnerability analysis and intrusion detection assignment. You have been provided with a stripped Linux binary at `/app/auth_daemon`. This legacy daemon processes authentication requests but has been flagged by the security team for suspicious behavior. It is suspected of being vulnerable to privilege escalation (CWE-78) and credential leakage via process command-line arguments (CWE-214) due to how it spawns subprocesses.

Your objectives are:
1. **Reverse Engineer the Binary**: Analyze `/app/auth_daemon` using the tools available in your environment (e.g., `objdump`, `strings`, `gdb`) to determine exactly how it constructs and executes commands when handling an authentication request. Identify the specific command-line structure, the binary it calls, and how the username and password fields are passed.
2. **Develop an Intrusion Detection Script**: Write a Python 3 script at `/home/user/detector.py` that can parse process execution logs and reliably detect invocations of this vulnerable pattern. The script must detect both the leaked credentials in the command-line arguments and any command-injection payloads that attempt privilege escalation through this specific execution path.

**Detector Specification:**
* Your script must be executable as: `python3 /home/user/detector.py <input_dir> <output_log>`
* `<input_dir>` will contain multiple JSON files. Each file represents a simulated process execution event (similar to `auditd` logs), containing a JSON array of the command-line arguments. For example: `["/bin/bash", "-c", "echo hello"]`.
* `<output_log>` must be a text file created by your script. For every file in the `<input_dir>` that matches the "evil" criteria (either a credential leak originating from the daemon's specific command format OR a command injection payload exploiting it), write the base filename of the JSON file on a new line in the `<output_log>`.
* Files that represent normal system activity (clean) should not be written to the output log.

Do not use hardcoded filename lists; your script must dynamically classify the content of the JSON files based on the malicious patterns you identified in the binary. The security team will run your script against a hidden adversarial corpus consisting of both normal activity and malicious/leaking invocations.