You are acting as a security researcher analyzing a simulated authentication service. 

There is a binary located at `/home/user/token_check`. This binary validates authentication tokens for users. It takes two arguments: a username and a token. If the token is valid for the given username, it grants access. The token validation relies on a hardcoded secret key embedded within the binary and a simple custom checksum algorithm.

Your task is to:
1. Reverse engineer or analyze the `/home/user/token_check` binary to discover the hardcoded secret key.
2. Figure out the token generation algorithm used by the binary.
3. Write a C program located at `/home/user/forge.c` that takes a single command-line argument (a username) and prints the valid token for that user to standard output.
4. Compile your program to `/home/user/forge`.
5. Use your forged token generator to create a valid token for the username `admin` and save ONLY the token string to a file named `/home/user/admin_token.txt`.

Constraints:
- Do not modify the original `/home/user/token_check` binary.
- Ensure `/home/user/forge` is an executable compiled from your C code.
- The output file `/home/user/admin_token.txt` must contain exactly the token for the `admin` user and nothing else (no newlines).