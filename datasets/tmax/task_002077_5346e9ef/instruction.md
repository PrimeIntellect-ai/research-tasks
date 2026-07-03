You are acting as a forensics analyst and incident responder recovering from a recent breach. The attacker compromised our host via a vulnerable file upload handler, encrypted sensitive evidence, and left a ransom note. 

Your objectives are to recover the encrypted evidence and patch the vulnerable service.

Phase 1: Evidence Recovery
1. The attacker left an image file at `/app/evidence/ransom_note.png`. Extract the text from this image (you can use `tesseract`). It contains the prefix of the password used to encrypt the evidence.
2. The attacker's encryption tool was partially recovered. We know they used OpenSSL AES-256-CBC with PBKDF2. The password format is the exact prefix found in the image, followed immediately by a 3-digit number (e.g., if the prefix was "Pass", a password might be "Pass123").
3. The encrypted evidence is located at `/app/evidence/secret.enc`. Write a Go script or use bash tools (like a loop with `openssl`) to brute-force the 3-digit suffix and decrypt the file.
4. Save the successfully decrypted text to `/app/evidence/decrypted.txt`. This text contains a vital authorization token.

Phase 2: Remediation and Service Restoration
1. The compromised Go web service is located at `/app/server/main.go`. It contains a `/upload` endpoint that is susceptible to path traversal (it blindly trusts the `filename` from the multipart form).
2. Fix the `/upload` endpoint in `/app/server/main.go` so that it sanitizes the filename (e.g., using `filepath.Base`) and ensures files are only written inside the `/app/server/uploads/` directory.
3. Add a new endpoint to the server at `GET /token` that returns the exact contents of the token recovered in Phase 1 in plain text.
4. Start the patched Go server. It must listen on `localhost:8080`. Leave it running in the background.