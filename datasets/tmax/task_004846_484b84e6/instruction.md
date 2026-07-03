As a DevSecOps engineer, you are enforcing "Policy as Code" constraints on deployed binaries. Our build pipeline embeds a security policy payload directly into the ELF binary to ensure that environment configuration travels with the executable and can be verified.

Your task is to write a Go utility that extracts, decodes, and verifies this policy payload from an ELF binary. 

You have been provided with an ELF binary located at `/home/user/target_bin`.

Write a Go program at `/home/user/extractor.go` that performs the following steps:
1. Parse the ELF binary `/home/user/target_bin` (you can use the standard library `debug/elf` package).
2. Locate the specific custom section named `.sec_policy`.
3. Extract the raw bytes from this section. The contents are Base64 encoded.
4. Base64-decode the extracted bytes to recover the original payload (which is a JSON string).
5. Compute the SHA-256 hash of the decoded payload bytes.
6. Write the results to `/home/user/verification_log.json`. 

The output file `/home/user/verification_log.json` must contain exactly one JSON object with two keys: `extracted_policy` (containing the decoded JSON object itself, NOT a string literal) and `sha256` (containing the lowercase hex-encoded SHA-256 hash of the decoded payload).

For example, if the decoded payload is `{"role":"web"}` and its SHA256 hash is `abc...`, your output file should look structurally like this:
```json
{
  "extracted_policy": {
    "role": "web"
  },
  "sha256": "abc..."
}
```

You are restricted to using Go's standard library. Once you write the code, execute it so the output file is generated correctly.