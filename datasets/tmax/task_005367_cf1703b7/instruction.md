I'm a storage administrator trying to manage disk space on our legacy logging server. We have a massive nested archive of old server logs, and I need an automated way to query its contents without extracting it, as we simply don't have the disk space to unpack it.

I need you to build a Go-based HTTP service that dynamically analyzes this nested archive via streaming I/O. 

Here are the details:
1. **The Archive**: There is a nested archive located at `/app/server_backup.tar.gz`. It contains multiple `.zip` files, which in turn contain various `.log` and `.dat` files.
2. **The Security**: The API needs to be protected. I lost the plaintext token, but I left a picture of the sticky note containing the token at `/app/auth_token.png`. You will need to extract the token from this image (you can use Tesseract OCR, which is installed).
3. **The Service**: Write and run a Go web server listening on `127.0.0.1:9090`.
4. **Endpoints**:
   - `GET /health`: Returns a `200 OK` status with the body `{"status": "ok"}`. (No authentication required).
   - `GET /largest`: Returns a JSON array of the top 3 largest files hidden deep within the `.zip` files inside the `tar.gz` archive. 
     - **Format**: `[{"path": "zipname.zip/filename.ext", "size": 123456}, ...]` sorted by size in descending order.
     - **Authentication**: Must require an `Authorization: Bearer <TOKEN_FROM_IMAGE>` header. Return `401 Unauthorized` if the token is missing or incorrect.
     - **Requirement**: You must use streaming I/O in Go (`archive/tar`, `compress/gzip`, `archive/zip`) to parse the nested structures. You cannot use shell commands to extract the archive to disk.

Please write the Go code, compile it, and start the service in the background so it continues running on `127.0.0.1:9090`. Wait for the service to be fully up before finishing the task.