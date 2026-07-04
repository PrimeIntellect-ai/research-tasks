You are a performance engineer tasked with replacing a legacy, unmaintained binary with a high-performance Go implementation. 

We have a stripped executable located at `/app/legacy_hasher`. This tool reads a stream of newline-separated strings from standard input and outputs a hex-encoded custom checksum for each line to standard output. 

Unfortunately, `/app/legacy_hasher` is notoriously slow and occasionally crashes under specific workloads. We have captured a core dump from one of its recent crashes, located at `/app/cores/core.legacy_hasher.12345`. There are also some container logs in `/app/logs/container.log` that might provide context on the input that caused the crash.

Your tasks are:
1. Analyze the core dump and logs to understand the crash and the internal workings of the custom checksum algorithm.
2. Reverse-engineer the custom hashing logic used by `/app/legacy_hasher`.
3. Write a fast, optimized, and crash-free replacement in Go.
4. Save your source code to `/home/user/fast_hasher.go` and compile it to `/home/user/fast_hasher`.

Your implementation must read newline-separated strings from standard input and write the corresponding hex-encoded checksums to standard output, matching the exact behavior of the legacy binary (but without crashing on the edge cases). The output must be BIT-EXACT to the correct checksum logic for any given input.

To verify your implementation, write a regression test script in `/home/user/test_harness.sh` that feeds varied inputs to both `/app/legacy_hasher` and `/home/user/fast_hasher` (avoiding the known crash inputs for the legacy binary) and diffs their outputs.

Ensure your compiled binary is executable and located exactly at `/home/user/fast_hasher`.