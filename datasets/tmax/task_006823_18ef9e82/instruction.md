You are a forensics analyst investigating a compromised host. You have discovered a local Go web server left behind by the attacker, apparently used to stash compromised credentials in memory.

The server is currently running on `127.0.0.1:8080`. The source code for this server has been recovered and is located at `/home/user/server.go`. 

Your investigation indicates that the attacker's server has a `/evidence` endpoint that requires JWT authentication. However, a quick review of the code suggests there might be a flaw in how the server handles JWT signature verification, specifically related to the algorithm type.

Your task is to:
1. Analyze the Go source code at `/home/user/server.go` to understand the authentication logic and expected token claims. You must authenticate as the `admin` user with the `forensics` role.
2. Exploit the JWT vulnerability to bypass the signature check and retrieve the JSON payload from `http://127.0.0.1:8080/evidence`.
3. The response will contain a JSON object mapping usernames to their MD5-hashed PINs. Extract the hash for `target_user`.
4. Crack the hash for `target_user`. It is known to be a 4-digit numeric PIN (0000-9999).
5. Save your findings to a file named `/home/user/recovery.json`. The file must be strictly valid JSON in the following format:
```json
{
  "forged_token": "<the exact JWT string you used to bypass authentication>",
  "target_user_pin": "<the cracked 4-digit PIN>"
}
```

Ensure that your `forged_token` consists of three dot-separated parts (Base64Url encoded), even if the signature is empty.