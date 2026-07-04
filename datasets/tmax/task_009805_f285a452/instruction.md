You are a network engineer analyzing a suspicious custom network client. You have intercepted its traffic and isolated its executable. 

During your packet inspection, you observed the client communicating over TLS using a custom certificate chain. You managed to extract the server's certificate chain from the traffic, but you need the Root CA to verify it. You suspect the Root CA is hardcoded directly inside the client's ELF binary.

You have been provided with the following files:
1. `/home/user/client_bin` - The stripped ELF executable of the custom client.
2. `/home/user/traffic_certs.pem` - The server's certificate chain (leaf certificate followed by the intermediate certificate) extracted from the TLS handshake.

Your objectives are:
1. Analyze the `client_bin` ELF executable and extract the embedded Root CA certificate (in PEM format). Save this extracted certificate exactly as `/home/user/extracted_root.pem`.
2. Validate the certificate chain in `traffic_certs.pem` using the extracted Root CA.
3. Extract specific metadata from the certificates.
4. Generate a final JSON report at `/home/user/report.json` with the following structure:
```json
{
  "root_ca_subject": "<Full Subject string of the extracted Root CA, exactly as output by openssl x509 -subject -noout>",
  "leaf_cn": "<Common Name (CN) of the leaf certificate from traffic_certs.pem>",
  "leaf_serial": "<Serial Number of the leaf certificate in UPPERCASE HEX without '0x' prefix>",
  "chain_valid": <true or false boolean, representing if the traffic_certs.pem chain is valid against the extracted_root.pem>
}
```

Ensure your JSON file is well-formed. Use whatever scripting or command-line tools you prefer (e.g., Python, Bash, OpenSSL, readelf, strings) to complete this task.