You are acting as a penetration tester and security developer. We have an in-house C application for processing secure file uploads, located at `/app/secure_uploader_src`. This tool decodes base64-encoded payloads, validates a client certificate chain, and writes the decoded output to an isolated sandbox directory.

However, during a recent security audit, we discovered that the application is vulnerable. Specifically:
1. The base64 decoding routine in `decoder.c` has a flaw that mishandles padding, occasionally truncating valid data.
2. The file writing logic in `handler.c` is susceptible to a path traversal attack, allowing malicious filenames (e.g., containing `../`) to escape the sandbox directory.
3. The sandboxing mechanism (using `seccomp` in `sandbox.c`) has a misconfigured rule that fails to restrict file writes to the intended directory correctly due to a missing environmental variable check.

Your task is to:
1. Analyze the C source code in `/app/secure_uploader_src`.
2. Fix the path traversal vulnerability by ensuring any filename containing `../`, `..`, or absolute paths starting with `/` are rejected (the program should return an exit code of 2).
3. Fix the base64 decoding logic to correctly handle standard padding without truncation.
4. Fix the build script (`Makefile`) which is currently missing an include path for the crypto library needed for the certificate validation.
5. Compile the fixed application to `/home/user/secure_uploader_fixed`.

The compiled binary `/home/user/secure_uploader_fixed` must take three arguments: `<base64_payload> <filename> <cert_path>`. It should behave exactly like the reference secure implementation.

Please fix the source code and compile the final binary.