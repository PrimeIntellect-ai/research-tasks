You are a forensics analyst responding to a server compromise. The attacker exfiltrated web traffic logs and HTML snippets, filtering them to find vulnerable payloads. They used a custom command-line tool to generate integrity hashes for the files they successfully exploited. 

We have recovered this tool at `/app/auth_tool`. It is a stripped ELF binary.
We also recovered a sample dataset of the intercepted HTML snippets in the directory `/app/evidence/`.

Your objective is to build a Python tool that recreates the attacker's forensic pipeline to identify exactly which files were flagged for exfiltration.

Write a self-contained Python script at `/home/user/analyzer.py` that does the following:
1. Accepts two command-line arguments: an input directory path (containing HTML files) and an output CSV file path.
2. Scans all `.html` files in the provided input directory.
3. Implements Content Security Policy (CSP) enforcement. The script must identify which HTML files **violate** the following strict CSP:
   `default-src 'self'; script-src 'self' https://cdn.trusted.com; object-src 'none';`
   *Violations include: inline `<script>` tags (e.g., `<script>alert(1)</script>`), `<script src="...">` pointing to any domain other than `self` (relative paths) or `https://cdn.trusted.com`, and any `<object>` tags.*
4. For every file that **violates** the CSP, compute the attacker's custom integrity hash of the file's raw byte contents. 
   * You must reverse-engineer the hashing algorithm used by `/app/auth_tool`. You can pass files to `/app/auth_tool` to observe its inputs and outputs, or analyze its binary structure.
   * You MUST reimplement the hashing algorithm natively in Python.
5. Output a CSV file to the specified output path. The CSV should have no header and contain rows formatted exactly as: `filename.html,hash_hex_string` (e.g., `snippet_42.html,a1b2c3d4`). Order the rows alphabetically by filename.

**Constraints & Evaluation:**
- During the automated evaluation, we will run your script on a hidden dataset of 10,000 files.
- `/app/auth_tool` **WILL BE DELETED** from the evaluation environment before your script is run. Your script must not depend on calling the binary via `subprocess` or similar means.
- Your script will be evaluated based on the accuracy of the output CSV compared to a ground-truth reference. You must achieve an accuracy of 1.0 (100% correct classification and hashing).