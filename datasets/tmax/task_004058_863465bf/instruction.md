You are an internal tools web developer tasked with building a highly reliable, chunked file-upload microservice using Python and gRPC. We've been experiencing "lifetime" issues with our current HTTP-based uploads where long-running connections drop or chunks get corrupted in transit without detection.

Your objective is to design and implement a gRPC service that allows clients to stream file chunks, validates the integrity of each chunk on the fly using checksums, and saves the fully assembled file.

Here is the precise specification of what you need to build:

1. Setup:
Create your project in `/home/user/upload_service`.
Create a directory for saved files: `/home/user/upload_service/storage`.

2. Protobuf Definition (`/home/user/upload_service/upload.proto`):
Create a protobuf file with `syntax = "proto3";` and `package upload;`.
Define a service named `FileUploadService` with an RPC method `UploadFile`. This method must accept a client-side stream of `UploadRequest` messages and return a single `UploadResponse`.
- `UploadRequest` must contain a `oneof payload` containing either:
  - `Metadata metadata = 1;`
  - `Chunk chunk = 2;`
- `Metadata` must contain:
  - `string filename = 1;`
- `Chunk` must contain:
  - `bytes data = 1;`
  - `uint32 crc32 = 2;` (The CRC32 checksum of this specific chunk's data)
- `UploadResponse` must contain:
  - `string message = 1;` (Can be "Success" or an error message)
  - `string sha256_checksum = 2;` (The hex digest SHA-256 of the fully assembled file)

3. Service Implementation (`/home/user/upload_service/server.py`):
Compile the protobuf file using `grpcio-tools`.
Implement the server listening on `[::]:50051`.
The server must handle the client streaming request:
- The first message in the stream *must* contain the `metadata`. If not, abort the gRPC context with `grpc.StatusCode.INVALID_ARGUMENT`.
- For all subsequent messages containing a `chunk`, compute the CRC32 of `chunk.data` (using `zlib.crc32(data) & 0xFFFFFFFF`).
- If the computed CRC32 does not match `chunk.crc32`, you must abort the stream using `context.abort(grpc.StatusCode.DATA_LOSS, "Invalid CRC32")`.
- As chunks arrive, append them to a file named `<filename>` in the `/home/user/upload_service/storage/` directory.
- Once the stream completes, calculate the SHA-256 checksum of the entire saved file on disk.
- Return an `UploadResponse` containing the final SHA-256 hex digest.

4. Client & Testing (`/home/user/upload_service/client.py`):
Write a script to test your server. It should generate a 5MB random binary file at `/home/user/upload_service/test.bin`, chunk it (e.g., 64KB chunks), compute the CRC32 for each chunk, and stream it to the server.
Print the returned SHA-256 checksum to stdout, and also write it to `/home/user/upload_service/result.txt`.

Ensure your server is left running in the background listening on port 50051 before you finish the task.