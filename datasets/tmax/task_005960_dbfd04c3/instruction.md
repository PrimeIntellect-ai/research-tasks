You are a forensics analyst investigating a compromised Linux host. The attacker used a clever technique to smuggle an exploit payload onto the system by embedding it within a custom X.509 TLS certificate chain. 

During your investigation, you extracted three PEM-encoded certificates from the malware's working directory, located at `/home/user/evidence/`:
- `ca.crt`: The root Certificate Authority (CA) used by the attacker.
- `cert_A.crt`: A leaf certificate.
- `cert_B.crt`: Another leaf certificate.

One of these leaf certificates is validly signed by the attacker's `ca.crt` and forms a proper certificate chain. The other is a decoy with an invalid signature.

The attacker embedded a hex-encoded exploit payload inside the **Organizational Unit (OU)** field of the Subject in the **valid** leaf certificate.

Your task:
1. Determine which of the two leaf certificates (`cert_A.crt` or `cert_B.crt`) is validly signed by `ca.crt`.
2. Write the filename of the valid certificate (e.g., `cert_A.crt` or `cert_B.crt`) to `/home/user/valid_cert.txt`.
3. Write a Rust program at `/home/user/recover.rs` that reads the valid certificate, extracts the hex-encoded payload from its Organizational Unit (OU) field, decodes the hex back into raw binary bytes, and writes the resulting binary payload to `/home/user/payload.bin`.
4. Compile and run your Rust program so that `/home/user/payload.bin` is generated.

You may use shell tools (like `openssl`) to investigate the certificates and identify the valid one, but the extraction and decoding of the payload must be implemented in the Rust program at `/home/user/recover.rs`. You can parse the certificate in Rust manually by searching for the OU field string, or by shelling out to `openssl` from within Rust, or by using a crate if you configure a Cargo project (though a single `.rs` file using standard library string/hex manipulation or `std::process::Command` is perfectly acceptable).

Ensure `/home/user/payload.bin` contains exactly the decoded bytes and nothing else.