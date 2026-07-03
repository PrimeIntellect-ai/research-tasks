You are a backup administrator tasked with archiving incremental changes from custom Write-Ahead Log (WAL) streams. We process millions of these streams, so we rely on a specialized C parsing library called `libwalparse` to handle the low-level format, and we build custom C++ tools on top of it.

Unfortunately, the vendored source for `libwalparse` version 1.0 located at `/app/libwalparse-1.0` is currently failing to build due to a small error introduced in the last commit. 

Your tasks are:
1. Fix the build issue in `/app/libwalparse-1.0` so that `make` successfully produces `libwalparse.a`.
2. Write a C++ program at `/home/user/archiver.cpp` that uses this library.
3. Compile your program to an executable at `/home/user/archiver`, statically linking against `/app/libwalparse-1.0/libwalparse.a`.

Your C++ program must do the following:
- Read a binary stream from `stdin`.
- Use the `parse_wal_frame` function from `walparse.h` to read frames in a loop until it returns `0` (indicating EOF or a parsing error).
- For each successfully parsed frame, check if the `page_id` is an EVEN number (simulating a differential filter).
- If `page_id` is even, compute the 8-bit XOR sum of all bytes in the frame's `data` payload.
- Write to `stdout` exactly 5 bytes for each even `page_id` frame: the 4-byte `page_id` (in little-endian, just as it was parsed) followed by the 1-byte XOR sum.
- Make sure to free the `data` buffer allocated by `parse_wal_frame` after processing each frame to avoid memory leaks.

The definition of the library function in `walparse.h` is:
`int parse_wal_frame(FILE* in, uint32_t* page_id, uint8_t** data, uint16_t* len);`
(Returns 1 on success, 0 on failure/EOF. It allocates `*data` which the caller must `free()`).

Ensure your compiled executable `/home/user/archiver` processes the standard stream correctly. Automated tests will verify your binary by piping thousands of randomly generated WAL streams into it and comparing the standard output byte-for-byte against our reference implementation.