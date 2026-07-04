You are a DevSecOps engineer responsible for enforcing "Policy as Code" in a CI/CD pipeline. Developers submit compiled artifacts along with encrypted metadata, and you need to automatically verify that these submissions do not violate security policies.

You have been provided with three files in the `/home/user` directory:
1. `/home/user/artifact.bin`: A compiled ELF executable.
2. `/home/user/metadata.enc`: A metadata file encrypted using the Fernet symmetric encryption scheme.
3. `/home/user/key.txt`: The base64-encoded Fernet key required to decrypt the metadata.

Your objective is to write a Python script at `/home/user/policy_check.py` that performs the following automated security checks:

**Step 1: Decryption**
Read the key from `/home/user/key.txt` and use the `cryptography.fernet` module to decrypt `/home/user/metadata.enc`. Parse the decrypted payload as a JSON object.

**Step 2: Injection / XSS Policy Check**
Iterate through all string values in the decrypted JSON object. The security policy strictly forbids any XSS payloads in metadata fields. Specifically, flag the metadata as violating policy if the exact substring `<script>` (case-insensitive) is found in any of the JSON string values.

**Step 3: Binary / ELF Policy Check**
Analyze the ELF binary `/home/user/artifact.bin` to determine if it dynamically imports or uses the dangerous `system` libc function. You can use any native Linux tool (e.g., `readelf`, `nm`, `objdump`) invoked from your Python script, or a Python module like `lief` or `pwntools` if you choose to install them. Flag the binary as violating policy if the `system` symbol is present.

**Step 4: Generate the Policy Report**
Your script must output the final results to a JSON file at `/home/user/policy_report.json` with the exact following schema and boolean values:

```json
{
    "metadata_decrypted": true,
    "xss_found": <true/false>,
    "banned_function_system_found": <true/false>,
    "policy_passed": <true/false>
}
```
*Note: `policy_passed` should only be `true` if `metadata_decrypted` is true, `xss_found` is false, and `banned_function_system_found` is false.*

Run your script to generate the `/home/user/policy_report.json` file.