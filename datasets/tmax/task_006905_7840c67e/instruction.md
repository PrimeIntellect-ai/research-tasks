You are a DevSecOps engineer implementing policy-as-code for a custom file upload handler. The upload handler was recently found to be susceptible to path traversal, and we need to retroactively scan a staging directory of uploaded artifacts.

You must write a Python script at `/home/user/check_policy.py` that evaluates the uploaded files against our security policies. 

The uploads are stored in `/home/user/uploads/`.
There is also a metadata file at `/home/user/metadata.json` which contains a JSON array of objects. Each object has the following keys:
- `filename`: The current name of the file in the `uploads` directory.
- `original_path`: The path provided by the user during upload.
- `csp_directive`: The Content Security Policy directive assigned to this artifact.

Your script must evaluate every file listed in `metadata.json` and flag it if it violates ANY of the following 3 security rules:
1. **Intrusion Detection (Path Traversal):** The `original_path` contains the substring `../`.
2. **Binary Analysis:** The file is a valid ELF executable (starts with the magic bytes `\x7fELF`) AND its binary contents contain the byte sequence `b'malicious_payload_x86'`.
3. **CSP Enforcement:** The `csp_directive` is anything other than exactly `"strict-dynamic"`.

Your script must create a text file at `/home/user/flagged.txt` containing the `filename`s of all flagged files. 
- Write one filename per line.
- The filenames must be sorted in alphabetical order.
- Do not include any other text in the output file.

You can assume the `uploads` directory and `metadata.json` already exist. Run your script to generate the `/home/user/flagged.txt` file.