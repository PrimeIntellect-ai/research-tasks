A runaway configuration backup script recently got stuck in an infinite loop due to a recursive symlink, generating a massive, corrupted configuration archive before it was killed. We need you to recover the original configuration and expose it via a secure local API.

Here are your instructions:

1. **Reconstruct the Archive**: In `/app/backup_parts/`, you will find a multi-part archive (`corrupt_backup.tar.gz.partaa`, `corrupt_backup.tar.gz.partab`, etc.). Recombine these parts and extract the contents.
2. **Clean the Configuration**: The extracted file `bloated_system.conf` contains millions of lines because the backup script repeatedly appended the same configuration block every time it followed the symlink. 
   - The original, correct configuration block starts with the line `[SYSTEM_CONFIG]` and consists of standard `key=value` pairs.
   - Extract *only the first instance* of this configuration block (ignore all the recursive duplicates that follow it).
3. **Recover the Auth Token**: There is an image located at `/app/api_token.png`. This image contains a printed authorization token. You will need to use OCR (e.g., `tesseract`) to read the token from this image. The token is the text immediately following "TOKEN:".
4. **Serve the Configuration**: Write and start an HTTP server (in the language of your choice) that listens on `127.0.0.1:9090`. 
   - The server must expose a `GET /api/config` endpoint.
   - The endpoint must require an `Authorization: Bearer <TOKEN>` header, where `<TOKEN>` is the exact string you recovered from the image.
   - If the token is missing or incorrect, return a `401 Unauthorized` status.
   - If the token is correct, return a `200 OK` status with the `Content-Type: application/json`. The response body must be a JSON object representing the key-value pairs from the cleaned configuration block.

Keep the server running in the foreground or background so it can be tested. Do not modify the original multi-part files.