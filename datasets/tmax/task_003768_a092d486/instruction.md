I need you to help me manage our disk space by building a custom log archiving tool in C++. We have massive hex-encoded log files that need to be converted to binary, chunked, and compressed using a legacy internal compression library.

You have access to the source code of our internal compression library, `liblogpack-1.2`, located at `/app/liblogpack-1.2`. Unfortunately, the previous admin left it in a broken state—it currently fails to build due to a configuration issue in its build files.

Your tasks are:
1. Identify and fix the build issue in `/app/liblogpack-1.2` so you can compile it into a static library (`liblogpack.a`).
2. Write a C++ program at `/home/user/archiver.cpp` and compile it to `/home/user/archiver`.
3. The `archiver` program must read standard input until EOF. The input will consist entirely of continuous uppercase hexadecimal characters (0-9, A-F) with no spaces or newlines (e.g., `48656C6C6F`).
4. Convert this hex string into raw binary data.
5. Split the raw binary data into chunks of exactly 4096 bytes. The final chunk may be smaller than 4096 bytes; do not pad it.
6. Compress each binary chunk using the `pack_data(const unsigned char* in, size_t in_len, unsigned char* out, size_t* out_len)` function provided by `logpack.h`. (Assume the output buffer for `pack_data` will never exceed `in_len * 2 + 16`).
7. Write the merged compressed data to standard output using the following custom binary format:
   - A global 8-byte header: `PACKv1\0\0` (the last two bytes are null terminators).
   - For each chunk, in order:
     - A 2-byte little-endian unsigned integer representing the uncompressed chunk size.
     - A 2-byte little-endian unsigned integer representing the compressed chunk size.
     - The raw compressed payload produced by `pack_data`.

Ensure your C++ program is robust and exactly matches the required binary output format, as it will be heavily tested against an oracle implementation. Do not output any debug text to standard output; standard output must contain only the final binary archive.