You are an backend web developer building an image processing feature. We have a legacy C library that extracts metadata from a custom binary image format. However, it is prone to memory safety issues (buffer overflows) and we suspect malicious actors are uploading crafted files to crash our servers.

Your task is to:
1. Fix the memory safety and undefined behaviour issues in `/app/c_src/extractor.c`. The code currently reads a length from the file header and copies data into a fixed-size buffer without bounds checking. Modify it so that it returns `-1` (error) when an invalid or out-of-bounds size is detected, instead of crashing.
2. Compile the fixed C code into a shared library `libextractor.so` and ensure the ABI matches what cgo expects. Place it in `/app/lib/`.
3. Write a Go CLI tool at `/app/filter.go` that uses cgo to call this library.
   - When run with a file path argument (e.g., `go run filter.go /path/to/input.bin`), it should pass the file's contents to the C function.
   - If the C function succeeds (returns 0), the Go program must exit with status 0 (clean).
   - If the C function fails (returns -1), the Go program must exit with status 1 (evil/malformed).
4. As part of a secondary feature, if the Go tool is run with the exact argument `--extract-image`, it must use Go concurrency and the `os/exec` package to run `tesseract` on `/app/sample.png`, capture the extracted text, and write the raw extracted string to `/app/recovered_text.txt`. Then exit with status 0.

Ensure your Go code handles memory safely and correctly bridges the C/Go boundary.