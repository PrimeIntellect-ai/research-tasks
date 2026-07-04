You are an engineer investigating a critical issue in a long-running data processing service written in Rust. The service has been crashing due to memory leaks, and we need to identify both the malformed input causing the leak and the leaked session ID from the resulting memory dump.

First, you need to build the service located in `/home/user/processor_service`. However, the previous developer left the build configuration incomplete. The project depends on a custom C allocator tracker (`libtracker.a` generated from `tracker.c`), but `cargo build` currently fails with a linker error (`undefined reference to 'track_allocation'`). Fix the Rust build configuration (e.g., `build.rs`) so that the project compiles successfully.

Once compiled, the service can process log files: `cargo run -- <logfile>`. 
We have a large log file at `/home/user/traffic.log` containing 500 requests. One specific line in this file triggers the memory leak and causes the program to crash, dumping its memory state to a file named `heap.raw` in the current directory.

Your tasks:
1. Fix the compilation error so the Rust service builds.
2. Use delta debugging/minimization techniques to isolate the exact single line from `/home/user/traffic.log` that causes the program to crash. Write this exact line (nothing else) to `/home/user/poison_line.txt`.
3. When the crash occurs, the service dumps its "leaked" memory to `heap.raw`. Analyze this binary memory dump file to extract the leaked session ID. The ID is embedded in a string formatted exactly as `LEAKED_SESSION_ID:<alphanumeric_string>`. Write ONLY the `<alphanumeric_string>` portion to `/home/user/leak_id.txt`.

Note: The system does not have root access, but all necessary tools (rustc, cargo, gcc, binutils) are available.