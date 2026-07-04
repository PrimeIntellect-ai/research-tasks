As a compliance analyst, you are tasked with generating audit trails for legacy system access logs. The old authentication system used a custom HTTP cookie integrity verification scheme that was only ever documented in a scanned internal memo.

You need to recreate the exact legacy cookie MAC generation tool to audit past HTTP sessions.

1. Inspect the scanned memo located at `/app/legacy_policy.png`. It contains the exact cryptographic algorithm, the Secret Salt, and the data formatting string used to sign the HTTP cookies.
2. Write a Python script at `/home/user/generate_audit_mac.py` that implements this exact logic. 
3. The script must take exactly two command-line positional arguments: `username` and `role`.
4. It must compute the MAC according to the parameters in the memo and print ONLY the resulting lowercase hex digest to standard output.

Do not print any extra text, debugging information, or newlines other than the final hex string, as your script will be rigorously tested against an automated audit tool with randomized inputs. Tesseract OCR is installed on the system if you need it.