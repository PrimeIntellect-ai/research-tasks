You are a performance engineer tasked with debugging a critical bottleneck in our data processing pipeline. We rely on a proprietary, legacy data processor located at `/app/processor` (a stripped binary). Recently, it has been causing severe CPU spikes and out-of-memory errors in production.

We suspect that specific, malformed payloads are triggering a catastrophic performance degradation (likely an infinite loop or massive allocation) inside the `/app/processor` binary. We have captured a memory dump from a crashed instance at `/app/crash.dmp`.

Your objective is to:
1. Analyze the `/app/processor` binary (using `objdump`, `strings`, `gdb`, etc.) and the `/app/crash.dmp` memory dump to determine the exact conditions that cause the binary to fail. The binary implements a custom header validation algorithm. There is a bug in the formula implementation inside the binary that causes the infinite loop when specific header constraints are violated.
2. Trace the intermediate state from the memory dump to extract examples of the "evil" payloads.
3. Create a minimal reproducible example to verify your understanding of the bug.
4. Write a Go program, `/home/user/filter.go`, that acts as a robust pre-filter. It must take a file path as its first command-line argument, read the file, and determine if it will trigger the performance bug in the processor.
   - If the file is safe to process, print exactly `CLEAN` to standard output.
   - If the file will trigger the bug, print exactly `EVIL` to standard output.

To succeed, your Go program must perfectly classify our internal testing corpora. The verifier will compile your Go program and run it against every file in our test suite. 

Ensure your `/home/user/filter.go` is fully self-contained and handles file reading robustly.