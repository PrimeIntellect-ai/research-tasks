You are acting as a security auditor for a legacy Linux system. We have discovered that several services are leaking sensitive credentials via command-line arguments, which are visible to any user who can read the `/proc` filesystem.

I have created a simulated snapshot of process data in `/home/user/proc_dump/`. 
Your task is to write a Rust program in `/home/user/auditor/` that scans this directory, decodes the leaked credentials, verifies the integrity of the process executables, redacts the sensitive data, and generates a secure JSON report.

Here are the exact requirements for your Rust application:

1. **Process Discovery**: Scan the `/home/user/proc_dump/` directory. Each subdirectory represents a PID (e.g., `/home/user/proc_dump/1001/`).
2. **Payload Decoding**: Read the `cmdline` file in each PID directory. The arguments are null-byte (`\0`) separated. Look for arguments starting with `--token=`. The value after the equals sign is a Base64 encoded string. You must decode this string.
3. **Sensitive Data Redaction**: Take the decoded token string and redact it. Keep the first 2 characters as plaintext, and replace all subsequent characters with asterisks (`*`), preserving the exact original length of the decoded string. (e.g., `secret` becomes `se****`).
4. **File Integrity Verification**: Each PID directory contains an `exe` file (simulating the binary). Calculate the SHA-256 hash of this `exe` file. Check if this hash exists in the authorized hashes list located at `/home/user/hashes.txt`.
5. **Report Generation**: Output the results to `/home/user/report.json`. The JSON must exactly match this structure:
   ```json
   {
     "csp_policy": "default-src 'none';",
     "findings": [
       {
         "pid": 1001,
         "redacted_token": "se****",
         "integrity_valid": true
       }
     ]
   }
   ```
   *Note: The `csp_policy` field is required as a simulated Content Security Policy enforcement for the downstream report viewer. Sort the `findings` array by `pid` in ascending numerical order.*

You will need to initialize a new Cargo project in `/home/user/auditor/`, write the code, build it, and run it to produce `/home/user/report.json`.