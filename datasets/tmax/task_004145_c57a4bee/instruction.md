You are acting as a compliance analyst generating secure audit trails. Your organization requires a lightweight, secure audit logging daemon. 

We have received an encrypted voicemail containing the emergency override token for this quarter. The audio file is located at `/app/voicemail.wav`. You must transcribe this audio file to retrieve the 4-digit numeric token.

Your task is to write and run a C-based TCP server that handles incoming audit payloads using this token.

Perform the following steps:
1. Transcribe the audio file `/app/voicemail.wav` to find the 4-digit token.
2. Write a C program at `/home/user/audit_server.c` and compile it to `/home/user/audit_server`.
3. The server must listen on `0.0.0.0:8080` for raw TCP connections.
4. The server must accept incoming requests in the exact format: `TOKEN: <4-digit-token> PAYLOAD: <base64_string>\n`
5. Security constraints:
   - Token validation: The server must compare the provided token to the token spoken in the audio file.
   - Payload decoding: If the token matches, the server must base64-decode the payload.
   - Secure coding (CWE-119): You must ensure your C code is resilient against buffer overflows. Do not use unsafe functions like `gets()`. Restrict input reading to 512 bytes.
6. Upon receiving a valid token, append the decoded payload (followed by a newline) to `/home/user/audit.log`, and reply to the TCP client with `SUCCESS\n`.
7. If the token is invalid or the format is wrong, reply with `AUTH_FAILED\n` and drop the connection.
8. Leave the compiled `/home/user/audit_server` running in the background so it can be verified.

Ensure the server stays running and correctly bound to port 8080.