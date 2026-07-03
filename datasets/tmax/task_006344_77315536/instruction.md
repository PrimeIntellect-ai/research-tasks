You are acting as an assistant to a network engineer who just intercepted some traffic containing authentication tokens. 

During a recent packet capture analysis, I extracted five token files that a client downloaded from an internal authentication server. I saved these files in the directory `/home/user/intercepted_tokens/`. 

We suspect the internal service is using weak cryptographic hashing for its authentication flow. Based on reverse engineering the client, we know the tokens are simple MD5 hashes of a plaintext string formatted as `admin:secret<N>`, where `<N>` is an integer between 0 and 100 inclusive (e.g., `admin:secret0`, `admin:secret42`, etc.).

I need you to:
1. Write a Go script at `/home/user/crack_token.go` that iterates through all the files in `/home/user/intercepted_tokens/`, generates the MD5 hashes for the possible plaintexts, and identifies which token file contains a valid hash matching the `admin:secret<N>` format.
2. Run your script to find the correct plaintext.
3. Once you find the correct plaintext, write ONLY the recovered plaintext string (e.g., `admin:secret42`) to a new file at `/home/user/valid_auth.log`.
4. As this is sensitive authentication data, enforce strict access control by changing the permissions of `/home/user/valid_auth.log` to exactly `0600` (read and write for the owner only).

Ensure your Go script handles file reading and cryptographic hashing properly.