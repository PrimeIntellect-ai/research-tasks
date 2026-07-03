You are acting as a security auditor tasked with securing a custom C-based web server. The previous developer left the company abruptly, leaving behind a partially compiled project and an intercepted voicemail. 

You need to perform the following steps:

1. **Analyze the Intercepted Audio:**
   There is an audio file located at `/app/intercepted_call.wav`. Transcribe this audio to discover the secret developer override token mentioned by the former employee.

2. **Reverse Engineer the Auth Module:**
   The source code for the authentication module is missing, but the compiled object file is available at `/home/user/auth.o`. Disassemble or analyze this file to understand how the override token from the audio is processed via the `Cookie` header.

3. **Audit and Patch the Web Server (`/home/user/src/server.c`):**
   The main server source code is provided in `/home/user/src/server.c`. You must fix several security issues:
   * **Open Redirect Vulnerability:** The login endpoint parses a `next` query parameter and blindly uses it in a `302 Found` `Location` header. Modify the code to ensure that the `next` parameter only redirects to relative paths starting with `/` (e.g., `/dashboard`). If an absolute URL or external domain (e.g., `http://evil.com`) is provided, default the redirect to `/home`.
   * **Sensitive Data Redaction:** The server currently logs all incoming HTTP headers directly to `/home/user/server.log`. Modify the logging function to inspect the `Cookie` header. If the developer override token (discovered from the audio) or any `session_id` cookie is present, redact their values in the log output, replacing the sensitive strings with `[REDACTED]`.

4. **Compile and Run:**
   Link your modified `server.c` with the existing `auth.o` to create the final executable `/home/user/server_secure`. 
   Run the server so that it binds and listens for HTTP requests on `127.0.0.1:8080`. 
   Keep the server running in the background.

Ensure your C code compiles cleanly without warnings. Do not modify the expected port or the log file path.