You are tasked with fixing a broken polyglot project and bringing up a network service that utilizes it. 

We have a C library intended to perform fast mathematical checksums using an architecture-specific assembly routine. However, the systems programmer left it incomplete. There is a linking error, and the assembly file is just a skeleton. Additionally, the configuration parameters for the system were left in an audio memo.

Here is your mission:

1. **Audio Decoding**: 
   There is an audio file at `/app/directive.wav`. Transcribe it. It contains a spoken semantic version requirement (the "API Version") and a numeric "cryptographic seed".

2. **Fix the C Library Linking and Assembly**:
   In `/home/user/project/`, you will find a `Makefile`, `libchecksum.c`, and an assembly file `checksum_x86_64.s` (using NASM syntax).
   - The Makefile currently fails to build `libchecksum.so` due to a linking error (missing symbol `asm_checksum`).
   - Fix the assembly file and the Makefile so that it successfully compiles into a shared library.
   - The assembly function `uint32_t asm_checksum(const uint8_t *data, size_t len, uint32_t seed)` must be implemented. The mathematical checksum algorithm is:
     `Final Checksum = seed + (sum of all bytes in data)`.
     Ensure it adheres to the standard System V AMD64 ABI.

3. **Polyglot Service Orchestration**:
   Write an HTTP server in any language of your choice (Python, Node.js, Go, etc.) that loads and binds to your compiled `libchecksum.so`.
   - The server MUST listen exactly on `127.0.0.1:8080`.
   - It must expose a `POST /compute` endpoint.
   - The endpoint will receive raw binary data in the request body.
   - The request will include an `X-Client-Version` header (e.g., `2.1.5`).

4. **Semantic Versioning & Response**:
   When a request hits `POST /compute`:
   - Compare the `X-Client-Version` against the "API Version" extracted from the audio.
   - The client is considered `compatible` if its version is greater than or equal to the API Version, AND has the same major version (e.g., if API Version is 2.1.0, then 2.1.5 and 2.9.0 are compatible, but 1.9.0 and 3.0.0 are not).
   - Calculate the checksum of the raw request body using your linked C library/assembly routine, passing the "cryptographic seed" from the audio as the seed argument.
   - Return a JSON response exactly in this format:
     `{"checksum": <integer>, "compatible": <boolean>}`

Do not exit your server process; it must remain running in the foreground or background so that an automated verifier can test the HTTP protocol responses.