You are a penetration tester auditing a custom web service written in Go. The source code for this service is located in `/home/user/server/main.go`, and its associated TLS certificates are in `/home/user/server/certs/`. 

Your objective is to analyze the service, identify its cryptographic and logical vulnerabilities, and write an exploit in Go to extract the secret flag. 

Here are the details of your assignment:

1. **Service Startup**: 
   Analyze the code in `/home/user/server/main.go`. Compile and run the service on the local machine. It will bind to `https://127.0.0.1:8443`.

2. **Certificate Validation**:
   The service uses a custom local certificate chain. You must inspect the leaf certificate (`/home/user/server/certs/server.crt`) and manually validate its chain against the intermediate or root provided in the directory. Extract the Common Name (CN) of the **Issuer** of the leaf certificate and write exactly that string to `/home/user/issuer.txt` (with no extra whitespace).

3. **Vulnerability Analysis & Exploit Development**:
   The service has a `/login` endpoint that accepts a `username` query parameter. It sets a secure, encrypted `auth_token` cookie that encodes the user's session.
   However, the developer made a critical error in how the session is encrypted (relying on AES-CTR without an integrity check like HMAC or GCM). 
   Write a Go program at `/home/user/exploit.go` that:
   - Connects to the `/login?username=guest` endpoint (ignoring self-signed TLS errors in the client).
   - Inspects the HTTP response to extract the `auth_token` cookie.
   - Performs a bit-flipping attack (a form of differential cryptanalysis on the keystream) on the decoded cookie. You must manipulate the ciphertext so that when the server decrypts it, the session reflects `username=admin` instead of `username=guest`.
   - Sends a request to the `/admin` endpoint using the forged `auth_token` cookie.
   - The `/admin` endpoint will return a flag if the cookie successfully decrypts to `username=admin`.

4. **Capture the Flag**:
   Take the flag returned by the `/admin` endpoint and save it to `/home/user/flag.txt`.

Ensure your exploit is fully functional and can successfully output the flag. You can write any additional helper files if needed, but the final output must precisely reside in `/home/user/issuer.txt` and `/home/user/flag.txt`.