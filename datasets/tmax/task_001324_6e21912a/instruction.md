You are a forensics analyst investigating a compromised Linux host. You have discovered a suspicious, stripped ELF binary located at `/app/c2_auth_check`. Analysis suggests this binary is used by a malware implant to perform custom TLS certificate chain validation and cryptographic checks on its Command and Control (C2) servers. It accepts a certificate file as an argument and returns exit code 0 if it belongs to the C2 network, or exit code 1 if it does not.

Your objective is to reverse-engineer or black-box analyze `/app/c2_auth_check` to determine the exact cryptographic and X.509 properties that define a "valid" C2 certificate. 

Once you understand the logic, you must write a standalone Python classifier tool that implements this exact validation logic natively. Your script will be used to sift through thousands of captured certificates to find more C2 infrastructure.

Write your script at `/home/user/detector.py`. 

Requirements:
1. Your script must accept two positional arguments: an input directory containing certificate files (in PEM format), and an output JSON file path.
   Usage: `python3 /home/user/detector.py <input_dir> <output_file.json>`
2. The output JSON must be a dictionary mapping the base filename of each certificate to either the string `"C2"` (if it matches the binary's criteria) or `"BENIGN"` (if it does not).
3. Your Python script **MUST NOT** invoke or call the `/app/c2_auth_check` binary. It must be a pure Python implementation of the logic. The automated testing environment will run your script on an isolated system where the binary is not present.
4. You may use any standard Python libraries or commonly installed crypto libraries like `cryptography`.

To complete the task, analyze the binary, deduce the specific combination of TLS certificate properties and hashes it checks, and correctly classify the test certificates.