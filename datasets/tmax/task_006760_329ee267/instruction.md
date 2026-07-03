You are a DevSecOps engineer tasked with analyzing a legacy web service, proving it is vulnerable, and then applying a secure policy-as-code fix.

A vulnerable Flask application is currently running on `http://localhost:8080`. The source code for this application is located at `/home/user/app.py`.

Your objectives are:
1. **Vulnerability Analysis & Exploit Crafting**: Analyze `/home/user/app.py` to discover a command injection vulnerability and an authentication constraint. The application requires a specific HTTP cookie to be present and formatted as a valid SHA256 hash.
2. **Payload Delivery**: Write and execute a script (in the language of your choice) that sends a crafted HTTP request to the running application. Your request must satisfy the cookie constraint and deliver an exploit payload via the vulnerable HTTP header. The payload must execute a system command that copies the file `/home/user/secret_key.txt` to `/home/user/pwned.txt`.
3. **Cryptographic Hashing**: Calculate the SHA256 hash of the contents of the newly created `/home/user/pwned.txt` file. Save only the resulting hex digest to a new file at `/home/user/hash_result.txt`.
4. **Secure Coding (Policy Enforcement)**: Create a patched version of the application and save it as `/home/user/fixed_app.py`. The new application must implement the exact same application logic (checking the cookie format and appending the IP address from the header to `/tmp/access.log`), but it must enforce a secure coding policy by strictly using native Python file I/O operations (e.g., `open()`) instead of any OS command execution functions (like `os.system`, `subprocess`, etc.). 

Ensure that your exploit succeeds and that `/home/user/fixed_app.py` is correctly written before finishing the task.