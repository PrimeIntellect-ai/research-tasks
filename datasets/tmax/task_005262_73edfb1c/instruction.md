You are tasked with deploying and fixing a local artifact curation manager. The system consists of an Nginx reverse proxy and a Rust-based artifact serving backend. Several parts of the system are incomplete or broken, and legacy data needs to be transformed.

Your working directory is `/app/artifact_manager/`.

Here are your objectives:

1. **Text Transformation and Encoding Conversion**:
   In `/app/artifact_manager/data/`, there is a legacy repository index named `manifest.legacy`. It is encoded in `ISO-8859-1` and uses a pipe-separated format (`filename|checksum|size`).
   You must convert this file to `UTF-8` encoding and transform it into a standard CSV format (comma-separated, with a header `File,Hash,Bytes`). Save the result to `/app/artifact_manager/data/manifest.csv`. You can use command-line tools like `iconv`, `awk`, or `sed` for this.

2. **Complete the Rust Backend (Streaming and Memory-Mapped I/O)**:
   The source code for the Rust backend is located in `/app/artifact_manager/rust_backend/`. It uses `axum`.
   The endpoint `GET /artifact/:name` is currently a stub. You must implement it so that it:
   - Reads the requested binary file from `/app/artifact_manager/data/binaries/<name>`.
   - Uses **memory-mapped I/O** to read the file (you must use the `memmap2` crate, which is already in `Cargo.toml`).
   - Returns the file content as the HTTP response body with the `Content-Type: application/octet-stream` header.
   - Returns a `404 Not Found` if the file does not exist.
   
   Compile the Rust application and ensure it runs, listening on `127.0.0.1:9000`.

3. **Configure the Services**:
   - Fix the Nginx configuration located at `/app/artifact_manager/nginx/nginx.conf`. It should listen on `127.0.0.1:8000`.
   - Route all requests starting with `/api/` to the Rust backend (which listens on `127.0.0.1:9000`), stripping the `/api` prefix (so `/api/artifact/foo.bin` goes to `/artifact/foo.bin` on the Rust server).
   - Start Nginx using this configuration file (e.g., `nginx -c /app/artifact_manager/nginx/nginx.conf`).
   - Start your compiled Rust backend in the background.

Verify your setup by requesting an artifact through Nginx:
`curl -s http://127.0.0.1:8000/api/artifact/test_artifact.bin --output test_download.bin`