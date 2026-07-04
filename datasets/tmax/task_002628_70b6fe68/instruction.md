You are a DevSecOps engineer responsible for enforcing Security Policy as Code. Your organization uses a centralized pre-commit hook to reject code that violates security standards or fails integrity checks.

Recently, the security team updated the master policy. The new policy details are distributed as an image artifact located at `/app/policy.png`. 

Your objective is to write a bash script, `/home/user/policy_check.sh`, that evaluates a given Python source file and decides whether to accept or reject it.

**Task Requirements:**
1. **Extract Policy Data:** Analyze the image `/app/policy.png` to find two critical pieces of information:
   - The `POLICY_SALT` (a specific alphanumeric string).
   - The `BANNED_CWE` (a specific CWE identifier, e.g., CWE-XXX).

2. **File Integrity Verification:**
   Every file submitted to your script will have a special header on its first line formatted exactly as:
   `# SIGNATURE: <sha256_hex_digest>`
   
   Your script must verify this signature. The valid signature is the SHA256 hash of a payload constructed by taking the **entire contents of the file excluding the first line**, and then appending the exact `POLICY_SALT` value to the end of that content (without adding any extra newlines). If the computed hash does not match the signature in the header, your script must reject the file.

3. **CWE Auditing:**
   The banned CWE represents OS Command Injection. Your script must scan the Python file to ensure it does not contain unsafe subprocess executions. Specifically, reject the file if you detect the usage of `os.system(...)` or the argument `shell=True` (with optional spaces around the equals sign) in `subprocess` calls.

4. **Execution and Output:**
   - Your script will be invoked as: `bash /home/user/policy_check.sh <file_path>`
   - If the file has a valid signature AND contains no banned CWE patterns, your script must exit with status code `0` (Accept).
   - If the file has an invalid signature OR contains a banned CWE pattern, your script must exit with status code `1` (Reject).

The grading suite will test your script against a hidden adversarial corpus of "clean" and "evil" Python files. You must achieve a 100% success rate on both corpora.