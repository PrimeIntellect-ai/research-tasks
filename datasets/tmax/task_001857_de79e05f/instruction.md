You are a security researcher analyzing a suspicious, partially corrupted binary and its associated source code. We suspect the original authors introduced a deliberate integer overflow (a form of numerical instability) and a concurrency flaw that occasionally deadlocks under high contention. 

We have recovered a vendored version of the open-source hashing library `smhasher` (specifically the Murmur3 implementation component) at `/app/smhasher`. However, the authors tampered with it:
1. The Makefile is broken, producing linker errors when you try to build the `murmur3_fuzzer` target.
2. They removed a critical security patch related to integer promotion during the final hash finalization phase, causing incorrect outputs on specific input lengths.
3. They added a multi-threaded wrapper (`parallel_hash.c`) that attempts to process multiple blocks concurrently, but it suffers from a deadlock due to misordered mutex acquisitions.

Your task is to fix the library and produce a standalone executable at `/home/user/fixed_hash`.

Requirements:
1. Diagnose and fix the compiler and linker errors in `/app/smhasher/Makefile`.
2. Inspect the git history of `/app/smhasher` to find a reverted commit labeled "Fix numerical instability in finalization step". Recover and apply this logic.
3. Use `gdb` or your preferred debugger to trace the execution of `parallel_hash.c`. Identify and fix the deadlock.
4. Compile your final fixed executable and place it exactly at `/home/user/fixed_hash`. It must read data from `stdin` and output the 32-bit hex hash to `stdout`.

Your final executable must be bit-exact in its runtime behavior to our recovered reference binary (an oracle). Automated verification will fuzz your binary against the oracle with thousands of random byte streams to ensure equivalence. Do not change the standard Murmur3 algorithm; just restore its proper function and fix the threading wrapper.