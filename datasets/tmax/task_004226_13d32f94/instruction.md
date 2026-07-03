You are helping a data researcher safely organize dataset archives received from untrusted third-party sources. Recently, several archives have been found to contain "Zip Slip" directory traversal attacks that attempt to overwrite files outside the intended extraction directory.

Your task is to build a C-based dataset scanner that detects malicious paths in tar archives.

Setup:
1. We are using the minimal C tar library `microtar` (version 0.1.0). Its source code is vendored at `/app/vendored/microtar-0.1.0`.
2. The provided build script for `microtar` is broken. You must fix it, compile the package, and produce a static library (`libmicrotar.a`) that your scanner can link against.
3. Test corpora are located at:
   - `/app/corpora/clean/` (benign datasets)
   - `/app/corpora/evil/` (malicious datasets containing path traversal attacks like `../`, `..\`, or absolute paths starting with `/`)

Requirements:
1. Fix the vendored `microtar` package so it compiles successfully into `libmicrotar.a`.
2. Write a C program at `/home/user/dataset_scanner.c` that includes the `microtar` header.
3. Your program must take a single command-line argument: the path to a tar archive.
   - Example: `./dataset_scanner /app/corpora/clean/dataset1.tar`
4. The program must iterate through all file headers in the archive.
5. If ANY file path in the archive contains a directory traversal attempt (e.g., `../`, `..\`) or is an absolute path (starts with `/`), the program must immediately print "MALICIOUS" to `stdout` and exit with status code `1`.
6. If the archive is completely free of directory traversal paths, the program must print "CLEAN" to `stdout` and exit with status code `0`.
7. Compile your program to an executable located at `/home/user/dataset_scanner`.

Ensure your scanner works perfectly against both the clean and evil corpora before completing the task. The automated verification will test your executable against these exact corpora.