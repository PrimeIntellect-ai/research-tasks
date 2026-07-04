You are acting as a security engineer tasked with rotating credentials and securing an internally developed file upload handler. 

We have a legacy C-based file upload service located at `/home/user/upload_svc`. The source code is provided in `/home/user/src/upload.c`. This service currently relies on a static token for authentication, which has been compromised. The old token is stored in a protected system file at `/etc/legacy_app/secret.token`.

Additionally, the developer left an image file at `/app/credential_clue.png`. This image contains a text string that is required to derive the new rotating credential.

Your objectives are:
1. **Analyze and Exploit**: The `upload.c` service has a known path traversal vulnerability in its filename handling. Compile the source code and use the vulnerability to read the contents of `/etc/legacy_app/secret.token`. 
2. **Recover Clue**: Extract the text hidden in the image `/app/credential_clue.png` (using `tesseract` or similar tools).
3. **Generate New Token**: Compute the SHA-256 hash of the concatenated string: `<extracted_text_from_image>:<contents_of_secret.token>`. This hex-encoded hash is your new secure token.
4. **Patch the Service**: Modify `/home/user/src/upload.c` to:
   - Fix the path traversal vulnerability. The service must reject any filename containing `../` or starting with `/`.
   - Update the authentication logic to require the newly generated token instead of the old static one.
5. **Output**: Save your patched C source code to `/home/user/src/upload_patched.c`. 

Your patched code will be compiled and evaluated against a suite of benign and malicious upload requests. To succeed, your patched program must achieve a perfect security and functionality score.