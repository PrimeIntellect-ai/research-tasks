You are a security engineer tasked with rotating the TLS credentials for a legacy internal service. 

The service relies on a custom authentication mechanism to authorize certificate rotations. The previous engineer left behind the source code for the validation binary at `/home/user/validator.c`, but lost the utility used to generate the authorization tokens.

Your objectives are:
1. Generate a new self-signed RSA 2048-bit certificate (`/home/user/cert.pem`) and private key (`/home/user/key.pem`). The certificate must have the Common Name `legacy.internal` and be valid for at least 365 days.
2. Analyze the provided `/home/user/validator.c` source code. The validator reads a certificate and a hex-encoded authorization token, decrypts the token using a custom, weak block cipher, and compares the result to the first 8 bytes of the certificate's SHA256 fingerprint.
3. Write a C program at `/home/user/generate_token.c` that performs the reverse operation (encryption). It should calculate the correct authorization token for your newly generated `cert.pem`.
4. Compile your C program, run it, and save the resulting 16-character hex string (representing the 8-byte token) to `/home/user/token.txt`.

The system will verify your success by compiling and running `validator.c` against your `cert.pem` and `token.txt`. 

Constraints & Requirements:
- You must use C to write the token generation tool (`generate_token.c`).
- Ensure no newline characters are at the end of `token.txt`.
- Do not modify `/home/user/validator.c`.
- You can use OpenSSL command-line tools and libraries (`libssl-dev`, `libcrypto`) as needed.