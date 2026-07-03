You are acting as a penetration tester auditing a local offline utility. 

You have been given access to a Python utility located at `/home/user/jwt_tool.py` which reads restricted system configuration. The utility requires a JSON Web Token (JWT) to authorize the user. Normally, it expects a token signed with a highly secure, unknown secret key. However, the code was written by a junior developer and contains a critical vulnerability regarding how it handles the JWT `alg` (algorithm) header.

Your objective is to:
1. Analyze `/home/user/jwt_tool.py` to understand its authorization requirements. It expects a user with the role of `superuser`.
2. Exploit the JWT algorithm vulnerability (specifically the "alg": "none" vulnerability) to bypass the signature validation. 
3. Create a valid, forged JWT token that grants you `superuser` access.
4. Run the utility using your forged token: `python3 /home/user/jwt_tool.py --token <YOUR_TOKEN>`
5. The tool will output a secret access key. Save this exact secret access key (just the key string, no extra text) to a file named `/home/user/access_key.txt`.
6. Apply strict file permissions to `/home/user/access_key.txt` so that it is exclusively readable by the owner (read-only, `chmod 400`).

Do not modify `jwt_tool.py`. You may write any auxiliary scripts (Bash, Python, Node, etc.) to help you generate the token. Ensure your final file `/home/user/access_key.txt` contains the correct secret and has the `0400` permission.