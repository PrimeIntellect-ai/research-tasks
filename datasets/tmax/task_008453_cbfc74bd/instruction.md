You are a DevSecOps engineer enforcing security policies for a custom C++ web application. We recently experienced a path traversal attack via our file upload handler, and the attacker may have left weak SSH keys as a backdoor.

Your task involves fixing the code, analyzing the compiled binary, and hardening the local SSH configuration.

Step 1: Fix the Vulnerability
The source code for the upload handler is located at `/home/user/upload_server.cpp`. It contains a function with the exact signature:
`void save_uploaded_file(std::string filename)`
This function is vulnerable to path traversal because it blindly concatenates the filename. Modify `/home/user/upload_server.cpp` so that if `filename` contains the substring `..` or the character `/`, the function returns immediately without attempting to open or write to any files. Do not change the function signature or remove other includes.

Step 2: Binary Analysis
Compile your fixed source code using the following command:
`g++ -O2 /home/user/upload_server.cpp -o /home/user/upload_server`
Analyze the resulting ELF binary (`/home/user/upload_server`) to find the exact mangled symbol name for the `save_uploaded_file` function.

Step 3: SSH Hardening
The user's authorized keys file is located at `/home/user/.ssh/authorized_keys`. According to our new policy as code, the `ssh-rsa` key type is deprecated. Remove any lines in this file that use the `ssh-rsa` algorithm. Keep all other secure keys (like `ssh-ed25519`).

Step 4: Reporting
Create a report at `/home/user/security_report.txt` with exactly three lines:
Line 1: The exact mangled symbol name of the `save_uploaded_file` function extracted from the compiled binary.
Line 2: The SHA256 checksum of your fixed `/home/user/upload_server.cpp` (just the hash, no filenames or spaces).
Line 3: The number of keys remaining in `/home/user/.ssh/authorized_keys`.