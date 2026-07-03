You are a security engineer tasked with recovering and rotating credentials for an offline legacy system. The system's authentication service has failed, but you have access to its client components and certificates.

In your home directory (`/home/user/`), you will find:
1. A directory `certs/` containing a Certificate Authority file (`ca.crt`) and three client certificates (`client1.crt`, `client2.crt`, `client3.crt`). Due to poor key management, two of these client certificates are invalid (either expired or not signed by the provided CA). 
2. A compiled executable binary named `legacy_auth`. This is the old client authenticator, which is known to contain a hardcoded fallback administrative token.

Your task is to:
1. Validate the certificate chain to identify the single valid client certificate signed by `ca.crt` that is not expired.
2. Reverse engineer or inspect the `legacy_auth` binary to extract the hardcoded fallback administrative token (it is a string containing numbers, letters, and special characters).
3. Craft an authentication payload and save it to a file exactly at `/home/user/payload.txt`.

The contents of `/home/user/payload.txt` must be exactly one line with the following format:
`<VALID_CERT_FILENAME>:<HARDCODED_TOKEN>`

For example, if the valid cert is `client1.crt` and the token is `Secret123!`, the file should contain exactly:
`client1.crt:Secret123!`

Do not include any other text or newlines in the file. You may use any command-line tools available in a standard Linux environment (like `openssl`, `strings`, `objdump`, etc.) to find the necessary information.