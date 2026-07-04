I need to build an OCR microservice for our web application to extract text from uploaded documents. I want you to implement a gRPC client and server in Go to handle this.

Here are the specific requirements:

1. **Protobuf Definition**:
   - Create a file named `ocr.proto` in `/home/user/workspace/proto`.
   - Define a gRPC service named `OcrService` with a single method `ExtractText`.
   - The request message should contain the image payload (as bytes) and a `crc32` field (as uint32).
   - The response message should contain the extracted `text` (as string).
   - Use `proto3` syntax and set the `go_package` option appropriately.

2. **gRPC Server**:
   - Create a Go server in `/home/user/workspace/server/server.go`.
   - The server must listen on `localhost:50051`.
   - When receiving a request, it must first calculate the CRC32 (IEEE) checksum of the image payload. If it does not match the provided `crc32`, return a gRPC error with code `InvalidArgument`.
   - If the checksum is valid, the server should process the image using the `tesseract` command-line tool (which is preinstalled) to extract the text. You can write the bytes to a temporary file and invoke `tesseract` via `os.Exec`.
   - Return the extracted text in the response.

3. **gRPC Client**:
   - Create a Go client in `/home/user/workspace/client/client.go`.
   - The client must read the image file located at `/app/invoice.png`.
   - Calculate the CRC32 (IEEE) checksum of the file's contents.
   - Send the gRPC request to the server.
   - Write the exact returned text to a file at `/home/user/extracted.txt`.

4. **Build and Execution**:
   - Initialize a Go module in `/home/user/workspace`.
   - Compile the protobuf file using `protoc` and the Go gRPC plugins.
   - Run the server in the background and then run the client to process `/app/invoice.png`.
   - Ensure the final extracted text is successfully saved to `/home/user/extracted.txt`.

Please set up the project structure, write all the necessary code, generate the stubs, and execute the workflow so that `/home/user/extracted.txt` is created with the correct OCR output.