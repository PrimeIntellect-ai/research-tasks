You are a security engineer preparing to rotate credentials for an internal service. Before deploying the new credentials, you need to audit an old key generation script, recover the lost seed used for the previous key, and validate the new certificate chain.

You have been provided with the following files in `/home/user/`:
1. `/home/user/generate_key.py`: A legacy Python script used to generate credential keys. It uses a custom pseudo-random number generator.
2. `/home/user/old_key.txt`: Contains a single integer, which is the output of `generate_key.py` used for the active credentials.
3. `/home/user/bundle.pem`: A PEM-formatted certificate chain containing a leaf certificate, an intermediate CA, and a root CA.

Your task is to perform the following steps:
1. **CWE Identification**: Audit `generate_key.py` and identify the most specific MITRE CWE identifier for the vulnerability of using a cryptographically weak pseudo-random number generator.
2. **Cryptanalysis**: Reverse the linear congruential generator algorithm in `generate_key.py` to find the original integer `seed` that produced the key found in `old_key.txt`.
3. **Certificate Validation**: Validate the certificate chain in `bundle.pem`. If the chain is valid (the leaf is signed by the intermediate, which is signed by the root), extract the Common Name (CN) of the leaf certificate.

Once you have gathered this information, create a JSON report at `/home/user/rotation_report.json` with the exact following keys:
- `"cwe"`: A string containing the CWE identifier (e.g., `"CWE-123"`).
- `"seed"`: An integer representing the recovered seed.
- `"cert_cn"`: A string containing the Common Name (CN) of the leaf certificate in `bundle.pem`.

Example format for `/home/user/rotation_report.json`:
```json
{
  "cwe": "CWE-338",
  "seed": 999999,
  "cert_cn": "example.com"
}
```