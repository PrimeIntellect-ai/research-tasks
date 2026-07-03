You are an application storage administrator managing a constrained environment where disk space is heavily limited. A highly active legacy application writes critical event logs to a fast-rotating file.

A background service is currently running and continuously generating these logs, writing them directly as a compressed stream to `/home/user/app/logs/rotating.log.gz`. Because disk space is low, this file is continuously appended to and periodically truncated by a racing rotation script.

Your task is to build a Python HTTP service that provides real-time visibility into the latest logs, handling the active gzip stream and the custom binary format without crashing when the file is rotated or when a gzip stream is truncated mid-write (a race condition).

Create a Python script at `/home/user/app/server.py` and run it. It must do the following:
1. Start an HTTP server listening on `127.0.0.1:8080`.
2. Expose a single endpoint: `GET /latest-events`.
3. When `GET /latest-events` is requested, the server must open `/home/user/app/logs/rotating.log.gz` and decompress the stream.
4. Parse the binary format contained within the uncompressed stream. The binary format consists of a sequence of records. Each record has:
   - Magic bytes: `E`, `V`, `T`, `\x01` (4 bytes)
   - Payload length: Unsigned 32-bit integer, Big-Endian (4 bytes)
   - Payload: A UTF-8 encoded JSON string of the exact length specified above.
5. Due to the race condition between the background writer and your reader, the gzip file or the internal binary format might end abruptly. You must catch any gzip EOF errors or incomplete binary reads and safely ignore the partial record at the end of the file.
6. The endpoint must return an HTTP 200 response with a JSON array containing all successfully extracted JSON payload objects from the file. Add the `Content-Type: application/json` header.

Do not stop the background log generator. Ensure your HTTP server remains running so it can be queried by the verification suite.