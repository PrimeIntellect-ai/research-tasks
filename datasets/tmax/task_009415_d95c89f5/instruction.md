You are a DevSecOps engineer responsible for enforcing deployment policies as code. You need to write a C++ program that validates incoming binaries before they are deployed to our edge nodes. 

We embed metadata directly into the ELF binaries of our applications. Specifically, every compliant application binary contains two custom ELF sections:
1. `.csp_policy`: Contains the Content Security Policy (CSP) string for the application's embedded webview.
2. `.cert_chain`: Contains a PEM-formatted certificate chain (leaf certificate and any intermediates) proving the binary's origin.

You must create a C++ program at `/home/user/validator.cpp` that performs the following validation on a target binary:

1. **ELF Analysis & Extraction**: Extract the contents of the `.csp_policy` and `.cert_chain` sections from the ELF binary provided as a command-line argument. (You may invoke shell utilities like `objcopy` from within your C++ code to assist with extraction).
2. **CSP Enforcement**: Inspect the extracted CSP string. The policy is considered **INVALID** if the `script-src` directive contains the strings `'unsafe-inline'` or `'unsafe-eval'`. 
3. **Certificate Chain Validation**: Validate the extracted certificate chain against our trusted Root CA located at `/home/user/root_ca.pem`. The chain in the ELF section might contain multiple certificates.

**Program Requirements:**
- Compile your program to `/home/user/validator` (e.g., `g++ -o /home/user/validator /home/user/validator.cpp`).
- The program should take exactly one argument: the path to the ELF binary.
- If the ELF file is missing required sections, or if the certificate chain is invalid, or if the CSP policy is insecure, the program must write exactly `DEPLOY_REJECTED` to `/home/user/deploy.log`.
- If all checks pass (the sections exist, the cert chain verifies against the root CA, and the CSP is secure), the program must write exactly `DEPLOY_APPROVED` to `/home/user/deploy.log`.

**Execution:**
Once your program is written and compiled, run it against the staged binary at `/home/user/target_app`:
`/home/user/validator /home/user/target_app`

Ensure `/home/user/deploy.log` is created with the correct decision.