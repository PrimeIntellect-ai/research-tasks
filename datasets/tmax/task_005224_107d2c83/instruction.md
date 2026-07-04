You are an open-source maintainer reviewing a pull request for a high-performance data processing pipeline. The original tool is a legacy binary, but a contributor submitted a PR to rewrite it using a Python driver, a Go-based concurrent worker pool, and a raw Assembly optimization for the hottest loop. 

Unfortunately, the PR is broken and fails to build and run correctly. Your task is to fix the project in `/home/user/repo` so that it flawlessly matches the behavior of the original legacy binary.

Here is the context of the broken PR:
1. **The Specification**: The exact magic XOR constant required for the data transformation was extracted from an old datasheet and saved as an image in `/app/spec.png`. You need to read this image (using OCR like `tesseract`) to find the integer value of the constant.
2. **Build System & Linking**: The `Makefile` is incomplete. It needs to compile a raw assembly file `math.s` into an object file, compile `worker.go` into a C-shared library `libworker.so`, and statically link the assembly object into the Go shared library.
3. **Go Concurrency**: The `worker.go` file attempts to process data chunks concurrently using goroutines and channels, but it currently suffers from a deadlock and drops the last few bytes of the input. You must fix the concurrency logic to ensure all chunks are processed and the results are correctly ordered.
4. **Assembly Analysis**: The `math.s` file contains a tiny function `apply_transform` that applies a bitwise operation. You must analyze it and ensure it's correctly exported and called by the Go code.
5. **Python Driver**: The entry point is `main.py`. It uses `ctypes` to load `libworker.so`. You need to fix the `ctypes` signatures and ensure it reads a binary file provided as a command-line argument, passes it to the Go library along with the magic constant from the image, and writes the transformed binary data directly to `stdout`.

**Requirements:**
- Fix the codebase in `/home/user/repo`.
- The entry point must be callable exactly like this: `python3 /home/user/repo/main.py <input_file>`
- It must output the exact same binary data to `stdout` as the legacy tool would.
- The Go code must utilize goroutines to process the data in chunks.
- Do not hardcode the expected output; implement the logic correctly.