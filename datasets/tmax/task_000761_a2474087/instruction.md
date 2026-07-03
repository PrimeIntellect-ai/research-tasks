You are a network engineer analyzing suspicious traffic on a local server. You have intercepted an HTTP request associated with an undocumented service, and you have also acquired a copy of the executable that handles these requests.

Your task is to analyze the intercepted HTTP request and the executable to extract and decrypt a hidden authentication token. 

Here are the details and your objectives:
1. The intercepted HTTP request is stored in `/home/user/traffic.txt`. Inside, you will find several headers, including a `Cookie` header containing a hex-encoded value labeled `Auth-Token`.
2. The executable that processes this token is located at `/home/user/handler.elf`. By analyzing this binary file, locate a hardcoded symmetric key. The key is a string that immediately follows the prefix `XOR_KEY_` (do not include the prefix in the key itself, only the characters that follow it up to the next null byte or newline).
3. The `Auth-Token` is encrypted using a repeating-key XOR cipher with the key you found in the binary. 
4. Write a Python script to decode the hex string and decrypt the token using the extracted key.
5. Save the final, plaintext decrypted string to exactly `/home/user/decrypted.txt` with no trailing newlines.

Constraints:
- Use standard command-line tools (like `strings`, `grep`, `cat`) and Python 3 to complete this task.
- Ensure the final output file contains only the decrypted token.