You are acting as a DevSecOps engineer for a custom Bash-based CI/CD pipeline. Your goal is to audit the existing pipeline scripts, reverse engineer a pre-compiled tool to audit it for backdoors, and enforce file permission policies.

The pipeline components are located in `/home/user/pipeline/`.

Perform the following tasks:

1. **Vulnerability Analysis & Patching**:
   Review the script `/home/user/pipeline/build_runner.sh`. It contains a severe vulnerability that allows arbitrary command execution. 
   - Identify the appropriate CWE (Common Weakness Enumeration) identifier for this exact vulnerability (e.g., CWE-XX).
   - Patch the script to remove the vulnerability while preserving its intended functionality (it should still build the provided target). Do not use `eval`.

2. **Reverse Engineering**:
   Analyze the binary `/home/user/pipeline/tools/validator`. This tool is used in the pipeline but has been flagged for potentially containing a hardcoded backdoor secret.
   - Reverse engineer the binary (e.g., using `strings`, `objdump`, or other tools) to extract the exact hardcoded authentication key used to bypass validation.

3. **Policy as Code Enforcement**:
   Write a bash script at `/home/user/enforce_policy.sh` that takes a directory path as its first argument. The script must scan the given directory recursively and:
   - Identify any files with the SUID or SGID bits set, and remove those bits.
   - Identify any world-writable files, and remove the world-writable permission.
   - For every file that had its permissions modified, append its absolute path to `/home/user/fixed_files.log`. Ensure the final `/home/user/fixed_files.log` is sorted alphabetically. 
   *(Note: You do not need to run this script on the pipeline directory, just write it so we can test it against a verification directory).*

4. **Reporting**:
   Create a JSON report at `/home/user/audit_report.json` containing the findings from steps 1 and 2. The JSON must have exactly this structure:
   ```json
   {
     "build_runner_cwe": "CWE-78",
     "validator_secret": "THE_SECRET_YOU_FOUND"
   }
   ```
   (Replace `CWE-78` and `THE_SECRET_YOU_FOUND` with your actual findings. Use the standard CWE format, e.g., "CWE-78" or "CWE-89").