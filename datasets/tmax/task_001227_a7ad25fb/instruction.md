You are a build engineer responsible for an artifact management system. We have a legacy C library that extracts version metadata from artifact filenames, which we are now exposing via a modern Python gRPC microservice.

However, the current C implementation has a memory safety bug (buffer overflow) when handling long filenames, and the integration pipeline isn't fully set up. 

Your tasks are to:

1. **Fix the C Code**: Edit `/home/user/workspace/artifact_utils.c`. The function `extract_version` is supposed to extract the prefix of a filename before the first underscore `_` and write it to a fixed 16-byte output buffer (`version_out`). Fix the code so it never writes more than 15 characters (plus the null terminator) to `version_out`, preventing buffer overflows.
2. **Polyglot Build Orchestration**: Create a script `/home/user/workspace/build.sh` (make it executable) that:
   - Compiles `artifact_utils.c` into a shared library named `libartifact.so`.
   - Compiles the provided `/home/user/workspace/artifact.proto` to generate Python gRPC stubs.
3. **gRPC & FFI Implementation**: Create `/home/user/workspace/server.py`. It should:
   - Use `ctypes` to load `./libartifact.so`.
   - Implement the `ArtifactManager` gRPC service defined in the proto file.
   - For the `GetVersion` RPC, call the C `extract_version` function, providing a 16-byte string buffer, and return the result.
   - Start the gRPC server on `localhost:50051` when executed (do not block forever if imported, only if run as `__main__`).
4. **Test Fixture**: Create `/home/user/workspace/test_client.py` that:
   - Connects to the gRPC server at `localhost:50051`.
   - Sends a `GetVersion` request with the filename: `"superlongversionstringthatwilloverflow_build123"`.
   - Writes the resulting version string extracted from the response to `/home/user/workspace/test_result.log` in the format: `Extracted: <version>`.

Note: You may need to install standard gRPC Python tools to compile the proto and run the server. Assume a standard Ubuntu environment with Python 3 and GCC.