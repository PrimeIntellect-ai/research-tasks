You are tasked with building a secure, custom backup agent for a Linux server. A recent log rotation system has caused issues with traditional backup tools, so you need to write a custom backup server in C that can dynamically search for, redact, and stream compressed logs over a network socket.

The authentication key for the backup server has been provided to you as an image of a security badge located at `/app/auth_badge.png`.

Your objectives:
1. Extract the authentication key from `/app/auth_badge.png`. The image contains a single line of text which is the key.
2. Write a C program that acts as a TCP server listening on `127.0.0.1:8888`.
3. When a client connects, the server should read exactly one line (up to the newline `\n` character). The expected format of this request is: `FETCH_BACKUP <AUTH_KEY>\n`
4. If the provided `<AUTH_KEY>` does not exactly match the key extracted from the badge, the server should immediately close the connection without sending any data.
5. If the key matches, the server must perform a backup of the directory `/app/data/`.
   - **Metadata search:** The server should only process files ending in `.log` within `/app/data/` that have a file size greater than 50 bytes (ignore smaller files, as they are artifacts of the racing log rotation process).
   - **Text editing / Redaction:** As the server reads the valid log files, it must redact sensitive information. Replace all occurrences of the string `SECRET_TOKEN=` followed by any 8 alphanumeric characters (e.g., `SECRET_TOKEN=A1b2C3d4`) with `SECRET_TOKEN=REDACTED`.
   - **Compressed Stream Processing:** The concatenated, redacted contents of all matching log files must be compressed using `zlib` (standard deflate) and streamed directly back to the client over the socket.
6. Once the compressed payload has been fully transmitted, the server should close the client connection but remain running to accept further requests.

You must write the server in C (e.g., `backup_server.c`), compile it (ensure you link against necessary libraries like `zlib`), and leave the process running in the background. Do not wrap the core logic in external bash scripts; the C program must handle the socket, the file reading, the redaction, and the zlib compression directly.

Please thoroughly test your server before finishing. You can use standard tools like `tesseract` to read the image, and `nc` or a small python script to test your server's response.