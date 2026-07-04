You are an infrastructure engineer tasked with automating the provisioning of user accounts and network routes via a GitOps pipeline. We have a legacy system that uses obfuscated configuration files (ending in `.enc`), and we need to ensure that no malicious commands or forbidden configurations are injected into our infrastructure when these files are pushed to our configuration repository.

Your goal is to build a robust C-based sanitizer, integrate it into a Git `pre-receive` hook, and write a daemon script that simulates the application of these configurations.

**Step 1: The Config Sanitizer (C)**
Write a C program at `/home/user/config_sanitizer.c` and compile it to `/home/user/config_sanitizer`. This program must read plaintext configuration lines from standard input (`stdin`).
It must allow (exit with code `0`) configurations that are entirely safe, and reject (exit with code `1` or higher) any configuration that is unsafe.

A configuration is **SAFE** if and only if every non-empty line strictly adheres to one of these two formats:
1. `useradd [username]` (where username consists only of lowercase letters and numbers, max 16 chars).
2. `ip route add [network]/[CIDR] via [gateway]` (valid IPv4 formatting).

A configuration is **UNSAFE** (and must be rejected entirely) if it contains:
- Any shell metacharacters (e.g., `;`, `&`, `|`, `$`, `>`, `<`).
- Any network route directing traffic via the forbidden gateway `10.99.99.99`.
- Any command other than the two allowed above.

*Note: Your sanitizer will be evaluated against a hidden adversarial corpus consisting of hundreds of clean and maliciously crafted configuration files. It must successfully accept 100% of the clean configurations and reject 100% of the malicious ones.*

**Step 2: The Obfuscation Decoder (Reverse Engineering)**
There is a stripped, proprietary binary located at `/app/config_decoder`. This binary takes an `.enc` file and decodes it into plaintext. You must reverse-engineer or black-box this binary to determine its command-line usage (it takes an input file and outputs plaintext). You will need this for the next step.

**Step 3: The Git Hook**
Initialize a bare Git repository at `/home/user/infra-configs.git`.
Create a `pre-receive` hook in this repository. The hook must:
1. Identify any files ending in `.enc` that are being modified or added in the incoming push.
2. Extract the blob contents of these `.enc` files.
3. Decode them using `/app/config_decoder`.
4. Pipe the decoded plaintext into your `/home/user/config_sanitizer`.
5. Reject the entire push if the sanitizer returns a non-zero exit code for *any* file.

**Step 4: The Provisioning Daemon**
Write a shell script at `/home/user/provision_daemon.sh`. This script should act as a mock system service. It must:
1. Accept a single argument: the path to a decoded plaintext configuration file.
2. Safely parse the file (simulating the execution of the `useradd` and `ip route` commands by appending a log line to `/home/user/provision.log` for each command in the format: `[SUCCESS] Applied: <command>`).
3. Ensure the script is executable.

Ensure all files are located exactly where specified and have the correct permissions. Do not use `sudo` or require root access.