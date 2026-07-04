You are a compliance analyst generating an audit trail for a legacy network. 

We have recovered an audio dictation from a former system administrator at `/app/compliance_audio.wav`. In this recording, the administrator lists three critical servers by name, the *last four characters* of their X.509 certificate SHA-256 fingerprints, and the CWE (Common Weakness Enumeration) ID of the primary vulnerability found in each server's respective codebase.

Your objectives:
1. **Transcribe and parse the audio:** Identify the three servers, their partial certificate fingerprints, and their assigned CWEs.
2. **Certificate Validation & Hashing:** Inspect the certificates located in `/app/certs/`. Identify which certificate belongs to which server based on the partial fingerprints dictated in the audio. Then, validate each certificate's trust chain against the root CA provided at `/app/certs/rootCA.pem`.
3. **CWE Code Auditing:** Inspect the source code snippets for each server located in `/app/code/`. Verify that the codebase actually contains the CWE mentioned in the audio. (The directories are named after the certificates, not the servers, so you must use the mapping from step 2).
4. **Generate the Audit Report:** Create a final integrated JSON report at `/home/user/audit_report.json`.

The JSON must follow this exact structure:
```json
{
  "server_name_from_audio": {
    "certificate_file": "filename.crt",
    "full_sha256_fingerprint": "the full lowercase hex sha256 fingerprint",
    "chain_valid": true, 
    "cwe_id": 79
  }
}
```
*Note: `chain_valid` should be a boolean (`true` or `false`) indicating if the certificate successfully validates against `rootCA.pem`.*

You may use any programming language or command-line tools (e.g., OpenSSL, Python, Whisper/SpeechRecognition) to complete this task. Write scripts as needed to process the data and generate the output.