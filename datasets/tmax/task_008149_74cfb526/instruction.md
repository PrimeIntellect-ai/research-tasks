You are an incident responder investigating a recent breach on a local Go-based internal service. The attacker managed to gain administrative access and drop a backdoor SSH key.

Here is what we know:
1. The service source code is located at `/home/user/app/server.go`. It handles authentication via JWTs (JSON Web Tokens). It relies on a custom JWT parser for a legacy integration.
2. The attacker bypassed the authentication by exploiting a vulnerability in how the JWT algorithms are handled (specifically an `alg=none` bypass).
3. The attacker added a persistent SSH key to the `user` account.

Your task:
1. **Analyze and Exploit**: Write a Go program at `/home/user/exploit.go` that, when run (e.g., `go run /home/user/exploit.go`), prints exactly one line to standard output: a forged JWT string that grants the role `"admin"` by exploiting the `alg="none"` vulnerability. The token payload must be `{"role":"admin"}`.
2. **Patch**: Fix the vulnerability in `/home/user/app/server.go`. Modify the `VerifyToken` function so that it explicitly rejects tokens where the algorithm is `"none"`, returning an `error` if `"none"` is used. Keep the rest of the valid verification logic intact.
3. **Remediate SSH**: Inspect `/home/user/.ssh/authorized_keys`. The file contains the legitimate admin key and the attacker's newly added key. Remove *only* the attacker's key (identifiable by its comment `hacker@pwned`). Ensure the legitimate key remains.

Constraints:
- You must use standard base64 encoding (URLEncoding without padding) for the JWT as per RFC 7519.
- Do not use external Go modules for `exploit.go`; use the standard library.