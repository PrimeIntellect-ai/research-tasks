You are a security engineer tasked with rotating credentials for our legacy backend systems.

We have received an image containing the emergency access password at `/app/emergency_password.png`. You will need to extract the password from this image (you can use `tesseract`).

Once you have the password, use it to decrypt the archive `/app/legacy_rotator.zip` (using `unzip -P <password> /app/legacy_rotator.zip -d /home/user/rotator`). This archive contains the source code for our legacy C++ credential rotation tool.

Upon reviewing the source code, you will notice several security flaws (CWEs), including improper file permissions handling and potential buffer overflows. Your task is to rewrite the credential rotator in C++.

We have provided a secure, compiled reference binary at `/app/oracle_rotator`. Your rewritten C++ program must be functionally equivalent to this oracle. It must accept the exact same command-line arguments and standard input, and produce the exact same standard output and exit codes. 

Compile your new tool to `/home/user/secure_rotator`.

The tool usage is:
`./secure_rotator <username> <new_password_hash>`
It reads the current credentials file (which has strict permission requirements: it must only be readable by the owner, otherwise the tool aborts with an error message) from standard input, updates the user's password hash if the user exists, and outputs the updated credentials file format to standard output. 

Ensure your C++ code is robust, fixes the CWEs, and compiles cleanly. Our automated test suite will aggressively fuzz your `/home/user/secure_rotator` against `/app/oracle_rotator` with thousands of random inputs to ensure bit-exact equivalence.