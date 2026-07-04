You are acting as a security auditor. We have discovered an undocumented and obfuscated file upload handler at `/home/user/app/handler.py`. 

Your objective is to audit this script, identify its vulnerabilities, and prove the impact.

Perform the following tasks:
1. **Reverse Engineer the Handler:** Analyze `/home/user/app/handler.py`. It uses a custom encoding/encryption layer to process incoming filenames and file contents. Figure out how the arguments are decrypted and processed.
2. **Identify the Vulnerability:** Determine the weakness in the file saving mechanism (hint: it's a very common file upload flaw).
3. **Exploit the Vulnerability:** Write a Python script at `/home/user/exploit.py` that, when executed, calls the `handler.py` script with the correct cryptographically encoded arguments. Your exploit must successfully write a file named `proof.txt` directly into `/home/user/` (i.e., `/home/user/proof.txt`), bypassing the intended upload directory. The contents of `proof.txt` must be exactly the string `EXPLOIT_SUCCESS`.
4. **Document Findings:** Create a JSON file at `/home/user/report.json` containing the vulnerability details and the cryptographic key you recovered from the handler. It must strictly follow this structure:
```json
{
  "cwe": "CWE-XX", 
  "xor_key": 0 
}
```
Replace `CWE-XX` with the correct official CWE identifier for this path traversal vulnerability (e.g., "CWE-79" for XSS, though this is not XSS). Replace `0` with the integer value of the XOR key used by the handler to decrypt the payloads.

Note:
* Do not modify the original `/home/user/app/handler.py`.
* Ensure your `exploit.py` runs without errors and invokes `handler.py` via a subprocess or by importing it (though subprocess is safer given the obfuscation).