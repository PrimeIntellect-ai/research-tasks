You are acting as a compliance analyst generating audit trails for a highly regulated environment. We recently lost the source code to our proprietary audit log extraction utility, but we still have a compiled version of it. For compliance reasons, we need to recreate this tool in Python so it can be audited and maintained.

Here is what you have to work with:
1. **The Policy Document**: A screenshot of the old compliance policy is located at `/app/policy_rules.png`. You will need to extract the XOR decryption key and the required HTTP cookie prefix from this image (you can use `tesseract` which is installed on the system).
2. **The Oracle Binary**: The original proprietary tool is located at `/app/oracle_extractor`. You can run it and pass it sample encoded payloads to observe its exact input/output behavior. 
3. **The Data Format**: The inputs to the program are base64-encoded payloads. When decoded and decrypted (using the XOR key from the image), they reveal an HTTP request log containing an ELF execution hash in the headers, along with various session cookies.

Your task is to write a Python script at `/home/user/audit_gen.py` that takes a single command-line argument (the base64 encoded payload) and outputs the exact same formatted audit string as the `/app/oracle_extractor` binary. 

Your script must:
- Accept the base64 string as `sys.argv[1]`.
- Base64 decode it.
- XOR decrypt it using the key found in the image.
- Parse the resulting string to find the ELF SHA256 hash and the value of the specific HTTP cookie prefixed with the string found in the image.
- Print the final correlated audit trail to stdout, exactly matching the format produced by `/app/oracle_extractor`. If the required cookie prefix is not present, or the payload is invalid, match the oracle's error output.

Our CI pipeline will aggressively fuzz your `/home/user/audit_gen.py` against the `/app/oracle_extractor` with thousands of random payloads to ensure bit-exact equivalence. Do not print any extra debugging information to stdout.