You are a security researcher analyzing a suspicious binary dropped on a compromised Linux system. You have recovered the source code of the dropper, but the attackers intentionally sabotaged it to prevent analysts from easily reconstructing their final payload.

Your workspace is located at `/home/user/investigation`.

Inside this directory, you will find:
1. `extractor.go` - The main Go program designed to parse log files, reconstruct the timeline of payload chunks, decode them, and write the final payload.
2. `decode.c` and `decode.h` - C files containing a custom decryption routine used by the Go program via CGO.
3. `auth.log` - The system log file containing the out-of-order payload chunks hidden within normal log entries.

The `extractor.go` program currently has several issues:
1. **Compiler/Linker Error:** When you try to build it (`go build`), it fails with a linker error related to the CGO integration.
2. **Timeline Reconstruction:** Even when compiled, the program incorrectly reconstructs the timeline of the chunks from `auth.log` because of a flaw in how it compares timestamps, leading to corrupted data.
3. **Encoding/Assertion Issue:** The Go code contains an assertion validation step that panics because the decoded data format doesn't match the expected transformation signature.

Your task is to:
1. Debug and fix `extractor.go` and/or the associated C files so that the program compiles successfully.
2. Fix the logical bugs causing incorrect timeline sorting and encoding/assertion failures.
3. Run the compiled `extractor` to generate the output file `/home/user/investigation/payload.bin`.
4. Calculate the SHA-256 hash of `/home/user/investigation/payload.bin` and save ONLY the hash string (lowercase hex) to `/home/user/investigation/flag.txt`.