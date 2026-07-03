You are an incident responder investigating a compromised Linux web server. The attacker has been exfiltrating data using a covert Command & Control (C2) channel hidden within Content Security Policy (CSP) violation reports sent over a custom TLS connection.

We have isolated the mechanism the attacker uses to encrypt these payloads. They relied on a standard Go library, but they tampered with the vendored code left on the server.

Your objectives:
1. Examine the vendored package located at `/app/vendor/github.com/Luzifer/go-openssl`. We suspect the attacker modified the OpenSSL salt header check (usually `"Salted__"`) to something else to break compatibility with standard tools. Identify the perturbation and fix the vendored source code to restore standard OpenSSL compatibility.
2. Write a Go program at `/home/user/decryptor.go` that reads a base64-encoded, OpenSSL-encrypted string from standard input (`stdin`), decrypts it using the passphrase `"CSP_Secret_Key_2024"`, and prints the raw plaintext to standard output (`stdout`). If an error occurs during decoding or decryption, your program must print nothing to standard output and exit with a non-zero status code.
3. Compile your program to `/home/user/decryptor`.

We have provided a stripped, reference binary at `/opt/oracle/decoder`. This is a known-good decryption tool recovered from the attacker's main infrastructure. Your compiled `/home/user/decryptor` binary must be bit-exact functionally equivalent to `/opt/oracle/decoder` for any given input.

Ensure your code handles arbitrary input gracefully (as our automated systems will fuzz your binary with random input to ensure its error handling perfectly matches the oracle).