You are a compliance analyst performing an audit on a legacy system. You need to extract a trusted root certificate from an old compiled binary, use it to validate a server's certificate chain, and then process a binary audit log if the chain is valid.

Your tasks are:
1. **ELF Analysis & Extraction**: Analyze the ELF binary `/home/user/legacy_processor`. There is a PEM-encoded root certificate embedded in a custom section named `.auth_root`. Extract this section's raw contents and save it to `/home/user/root_ca.pem`.
2. **Data Processing & Certificate Validation**: Write and run a Go script at `/home/user/audit_verify.go` that does the following:
   - Loads the root certificate from `/home/user/root_ca.pem`.
   - Parses and validates the certificate chain located at `/home/user/server_chain.pem` using the extracted root CA. The `server_chain.pem` file contains a leaf certificate followed by an intermediate certificate. You must verify that the leaf certificate is valid for the DNS name `audit.internal` and chains up to the root CA.
   - If (and only if) the certificate chain is completely valid, parse the binary audit file `/home/user/audit_data.bin`.
   - The `audit_data.bin` file contains a sequence of tightly packed records. Each record consists of:
     - A 2-byte Record Type (unsigned, Little Endian)
     - A 2-byte Length (unsigned, Little Endian)
     - A variable-length payload of `Length` bytes.
   - Iterate through the records to find the first record with a Record Type of `0x0077` (119 in decimal).
   - Read the payload of this record, interpret it as a UTF-8 string, and write it to a file named `/home/user/compliance_result.txt` in the exact format: `STATUS: VALID - PAYLOAD: <extracted_string>` (without a trailing newline).

If the certificate validation fails, your Go program should exit with an error and not write to the result file.