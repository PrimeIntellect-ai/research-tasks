You are a mobile build engineer maintaining our CI/CD pipelines. A critical step in our artifact deployment process involves transforming binary patch diffs of memory profiles to save bandwidth. The legacy C tool that performed this transformation was lost, and the pipeline is currently failing.

You need to recreate the tool in C. Write the source code to `/home/user/patch_transformer.c` and compile it to an executable at `/home/user/patch_transformer`.

Here are the requirements for the tool:
1. It reads raw binary data from `stdin` and writes the transformed binary data to `stdout`.
2. The data format starts with a 16-byte header:
   - Bytes 0-3: Magic number `0x50 0x41 0x54 0x43` ("PATC")
   - Bytes 4-7: Total payload length as a 32-bit unsigned integer (little-endian).
   - Bytes 8-15: Reserved (ignore).
3. Following the header is the payload. The payload must be processed in fixed-size blocks.
4. The block size is a critical configuration parameter. The previous engineer left a voice memo detailing the correct block size for the new mobile architecture. You can find this audio file at `/app/arch_config.wav`. Transcribe it to find the integer block size.
5. For each block in the payload, the tool must reverse the byte order of the block. If the final block is smaller than the block size, it should be reversed in place based on its actual size.
6. The tool must return exit code 0 on success, or 1 if the magic number is invalid or the input terminates unexpectedly before the specified payload length is reached.

Ensure your C code is memory-safe and efficient. Do not print any debug information to `stdout`, as it will corrupt the binary pipeline.