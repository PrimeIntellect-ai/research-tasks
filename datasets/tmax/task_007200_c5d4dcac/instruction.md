You are tasked with fixing a hybrid data processing pipeline that validates and decodes hex-encoded telemetry data. The previous team attempted to build this in Rust, but the Rust project failed to compile and was scrapped. The current version relies on a multi-file C project for heavy-lifting (checksum validation and hex decoding) and a Go program for concurrent orchestration.

Currently, the project in `/home/user/telemetry_pipeline` is broken. The C code fails to compile due to Makefile issues and a logical bug in the decoding phase, and the Go script deadlocks.

Here is what you need to do:

1. **Fix the C Project and Makefile**:
   - The C code is located in `/home/user/telemetry_pipeline/c_src/`.
   - The `Makefile` fails to build. Fix the compilation errors (look out for syntax errors in the Makefile and missing dependencies).
   - There is a logical bug in `decoder.c` inside the `hex_to_bytes` parsing logic. It causes out-of-bounds reads or incorrect decoding. Fix it so the C program correctly decodes hex strings to ASCII and validates the CRC32 checksum appended to the data.
   - The compiled C binary must be written to `/home/user/telemetry_pipeline/bin/decoder`.

2. **Fix the Go Concurrency Issue**:
   - The Go program `/home/user/telemetry_pipeline/go_src/orchestrator.go` reads `input_data.txt` and spawns goroutines to pass data to the C `decoder` via stdin. 
   - However, the Go program hangs indefinitely because of a channel/WaitGroup deadlock. Fix the Go code so it processes all records and exits cleanly.

3. **Process the Data**:
   - Run the fixed Go orchestrator. It will print valid decoded ASCII strings to standard output.
   - Save the standard output to `/home/user/telemetry_pipeline/decoded_output.txt`.
   - Sort the contents of `decoded_output.txt` alphabetically and save it to `/home/user/telemetry_pipeline/sorted_output.txt`.
   - Create a unified diff between `/home/user/telemetry_pipeline/expected.txt` and `sorted_output.txt`. Save this diff to `/home/user/telemetry_pipeline/diff.patch`.

Your task is considered successful when `diff.patch` is created and the C and Go files compile and run successfully without hanging or crashing.