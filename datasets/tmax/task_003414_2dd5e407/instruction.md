You are tasked with building the backend logic for an artifact manager that curates binary repositories. We receive nightly drops of compressed tar archives along with multi-line sync logs, and we need a service to verify, chunk, and serve these artifacts.

Your goal is to build a Rust application in `/home/user/artifact_manager` and configure an Nginx reverse proxy. 

**Part 1: The Rust Artifact Processor**
1. Read the upload log located at `/home/user/data/sync.log`. This file contains multi-line records formatted as:
   ```
   [START UPLOAD]
   File: <filename>
   Expected-Size: <bytes>
   [END UPLOAD]
   ```
2. For each file mentioned in the log, locate it in `/home/user/data/archives/`.
3. Verify the integrity of the archive. They are `tar.gz` files. If an archive is corrupt or invalid, skip it.
4. For each valid archive, split it into chunks of exactly 512,000 bytes (except the last chunk, which may be smaller). Name the chunks `<filename>.chunk.001`, `<filename>.chunk.002`, etc.
5. Save the chunks into `/home/user/data/chunks/`.
6. For each valid archive, create a symbolic link in `/home/user/data/active/` named `<filename>` that points to the original valid archive in `/home/user/data/archives/`.

**Part 2: The Rust HTTP API**
The Rust application must also run an HTTP server on `127.0.0.1:9000`. 
- It must respond to `GET /health` with an HTTP 200 OK and the text `System Operational`.

**Part 3: Service Composition (Nginx)**
Configure the local Nginx instance to run as a reverse proxy and static file server.
- Nginx must listen on `0.0.0.0:8080`.
- Requests to `http://localhost:8080/api/...` must be proxied to your Rust HTTP server on port 9000 (stripping the `/api` prefix so `/api/health` routes to `/health`).
- Requests to `http://localhost:8080/downloads/...` must serve files directly from the `/home/user/data/active/` directory.

Build your Rust project, configure Nginx, and leave both the Rust HTTP server and Nginx running in the background. Write a short completion log to `/home/user/finished.txt` when the system is ready for testing.