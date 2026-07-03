You are tasked with building the validation stage of a CI/CD pipeline for a custom Kubernetes operator. We have been receiving malicious payload injections, so we need a strict deployment validator written in C, along with automated scripts for deployment and firewall configuration.

You must perform the following tasks:

1. **Extract Configuration from Architecture Diagram:**
   There is a system diagram located at `/app/diagram.png`. Use `tesseract` to extract the text from this image. The image contains two critical pieces of information:
   - `ALLOWED_NAMESPACE: <namespace_name>`
   - `FW_PORT: <port_number>`

2. **Write a C-based Manifest Validator:**
   Write a C program at `/home/user/validator.c` and compile it to `/home/user/validator`. 
   The program must accept exactly one command-line argument: the path to a Kubernetes YAML manifest.
   It must read the file and enforce the following rules:
   - The manifest MUST contain `namespace: <namespace_name>` (where `<namespace_name>` is the exact string extracted from the diagram).
   - The manifest MUST NOT contain the string `privileged: true`.
   - The manifest MUST NOT contain the string `hostNetwork: true`.
   - The manifest MUST NOT contain the string `hostPath:`.
   
   If all conditions are met (the manifest is safe and targets the correct namespace), the program must exit with status code `0`. If any rule is violated, it must exit with status code `1`.

3. **CI/CD Pipeline Automation & Permissions:**
   Write a bash script at `/home/user/ci_pipeline.sh`. The script should:
   - Compile `/home/user/validator.c` to `/home/user/validator` using `gcc`.
   - Set the permissions of the `/home/user/validator` executable to exactly `711` (`rwx--x--x`).
   - Run the validator against all `.yaml` files in the directory `/app/corpora/clean/` and `/app/corpora/evil/`. 
   - Write a summary log to `/home/user/pipeline.log` listing the file paths and their pass/fail status (this file is for your own debugging; the automated verifier will call your C binary directly).

4. **Firewall Configuration Script:**
   Generate a bash script at `/home/user/fw_config.sh` that contains the precise `iptables` commands required to set up a PREROUTING rule in the nat table. The rule must forward incoming TCP traffic on port `80` to the `<port_number>` extracted from the diagram. Do not run this script (as you do not have root privileges), just create it with the correct commands.

Ensure your C code is robust and your bash scripts have execution permissions.