You are tasked with securing and deploying a legacy C++ JWT microservice. We recently discovered that our previous authentication binary was compromised, and we are migrating its functionality to a new vendored C++ package.

Your objectives:
1. **Reverse Engineering**: We lost the source code for the legacy authentication binary located at `/app/legacy_auth`. You must analyze this Linux ELF binary to extract the hardcoded 32-character HMAC secret key used for signing JWTs.
2. **Environment Configuration**: Save the extracted secret key inside a new file exactly at `/app/jwt-service/secret.key`.
3. **TLS Management**: The new service requires HTTPS. Generate a self-signed RSA 2048-bit TLS certificate and private key. Save them as `/app/jwt-service/tls/cert.pem` and `/app/jwt-service/tls/key.pem` respectively.
4. **Vulnerability Remediation**: The vendored package located at `/app/jwt-service` contains a known JWT "alg: none" bypass vulnerability in `src/auth.cpp`. Code review the file, identify the logic flaw that accepts unauthenticated tokens when the algorithm is set to "none" (or "NONE"), and patch it to reject such tokens.
5. **Compilation Fix**: The `Makefile` in the vendored package has a deliberate configuration error that prevents it from linking properly. Identify and fix the missing linker flags.
6. **Deployment**: Build the service by running `make` in `/app/jwt-service`. Then start the service. It is hardcoded to listen on `0.0.0.0:8443` and requires the TLS certificates and the `secret.key` file to be present.

Leave the service running in the background. Do not modify the expected endpoints or port. An automated testing tool will verify the service by attempting to authenticate using valid tokens, forged "alg: none" tokens, and tokens with invalid signatures.