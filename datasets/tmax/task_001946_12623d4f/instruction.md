You are an incident responder investigating a potential breach on a Linux system. You have discovered a rogue C++ authentication tool left behind by the threat actor in `/home/user/investigation/`. 

The attacker used this tool to generate access tokens. The tool reads a secret key from a system file that is no longer present, but you have managed to recover the C++ source code of the tool (`auth_service.cpp`) and a log of some intercepted tokens (`intercepted_tokens.txt`).

Your investigation objectives are:

1. **Cryptanalysis:** Analyze the custom cryptographic token generation logic in `auth_service.cpp` and use the known plaintext-ciphertext pairs in `intercepted_tokens.txt` to recover the missing secret key. Save the plaintext secret key to `/home/user/investigation/key.txt`.
2. **Token Generation:** Using the recovered key, forge a valid hex-encoded token for the username `system_admin`. Save this token exactly as a single line in `/home/user/investigation/forged_token.txt`.
3. **Injection Vulnerability Analysis:** The authentication service contains a severe logging vulnerability. Analyze the code to find a command injection flaw when validating failed tokens. Craft a specific `username` payload that, if processed by the validation routine, would successfully execute the command `touch /home/user/investigation/pwned` on the host. Save your exact username payload to `/home/user/investigation/payload.txt`.

You must create and populate the following files:
- `/home/user/investigation/key.txt`
- `/home/user/investigation/forged_token.txt`
- `/home/user/investigation/payload.txt`

You may write additional C++ or shell scripts to aid your cryptanalysis and token generation. Provide your findings accurately based on the provided source code.