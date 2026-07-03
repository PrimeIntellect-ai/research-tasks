You are assisting a technical writer in organizing a large batch of documentation and setting up a local documentation portal.

You need to perform the following steps:

1. **Extract and Organize Nested Archives:**
   There is a nested archive located at `/home/user/docs_archive.tar`. This archive contains several other archives (both `.zip` and `.tar.gz` formats) nested inside each other.
   Use shell commands to completely unpack all nested archives. Find every `.txt` file within the extracted contents and move them all into a single flat directory called `/home/user/organized_docs/`.

2. **Retrieve the Secret Project Codename:**
   The lead writer has left an audio dictation file for you at `/app/dictation.wav`. Process and transcribe this audio file to discover the secret project codename. The audio contains a short sentence stating the project codename clearly.

3. **Develop a Multi-Protocol Documentation Service:**
   Write a Python script at `/home/user/serve_docs.py` that concurrently runs two network services to serve the documentation. You must start this script so the services are running.

   **Service A: HTTP Documentation Server**
   - Must listen on `127.0.0.1:8080`.
   - Must serve the files located in the `/home/user/organized_docs/` directory via standard HTTP GET requests.

   **Service B: TCP Metadata API**
   - Must listen on `127.0.0.1:9090`.
   - Must accept raw TCP socket connections.
   - When a client connects, it will send commands terminated by a newline (`\n`).
   - If the client sends `AUTH <codename>\n` (where `<codename>` is the exact secret word found in the audio dictation in all uppercase), the server must respond with `OK\n`. 
   - If the client sends an incorrect codename, respond with `ERROR\n` and close the connection.
   - Once successfully authenticated, if the client sends `COUNT\n`, the server must respond with the exact number of `.txt` files inside `/home/user/organized_docs/` in the format: `FILES: <integer_count>\n`.

Ensure both servers are running simultaneously and reliably handle requests. The script should rely on standard Python libraries.