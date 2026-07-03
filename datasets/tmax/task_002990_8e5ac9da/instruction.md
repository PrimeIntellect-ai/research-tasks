You are a security auditor tasked with analyzing a custom permission validation mechanism for a client. The client uses a locally compiled binary to check encrypted permission tokens. You need to demonstrate that their token validation process is vulnerable to arbitrary execution, specifically bypassing authorization to read restricted files.

The client has provided the source code for the validator at `/home/user/validator.c`. 
They claim the token is safe because it is encoded. The token decoding process expects a Hex-encoded string. Once hex-decoded to raw bytes, every byte is XORed with the constant key `0x5A` to retrieve the final payload, which is then processed.

Your objectives:
1. Compile the provided source code to an ELF executable at `/home/user/validator`. Since this is an older system emulation, compile it with the following exact flags to disable protections that the client's legacy system lacks:
   `gcc -m64 -fno-stack-protector -z execstack -no-pie /home/user/validator.c -o /home/user/validator`
2. Analyze the compiled ELF binary to locate the memory address of the `grant_access` function.
3. Write a Python script at `/home/user/exploit.py` that crafts a malicious payload. The payload must exploit a buffer overflow in the token processing logic to overwrite the instruction pointer (RIP) and jump directly to the `grant_access` function. 
4. The Python script must output ONLY the final Hex-encoded string (after applying the XOR and Hex encoding steps expected by the binary).
5. Run the compiled `validator` binary, passing the output of your Python script as the first command-line argument.
6. The `grant_access` function, when successfully executed, will read the contents of `/home/user/secret_permissions.txt` and print it to standard output. Capture this output and save it to `/home/user/audit_report.txt`.

Ensure your `exploit.py` accounts for the 64-byte buffer and the saved frame pointer (RBP) before the return address. Use Python 3.