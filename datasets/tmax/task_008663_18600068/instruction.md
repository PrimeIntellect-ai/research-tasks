You are a DevOps engineer tasked with debugging a Rust-based log analysis utility called `log-tracer`. 

The source code for the project is located at `/home/user/log-tracer`. This tool is designed to read a log file, count the number of `ERROR` occurrences, and follow any trace directives (formatted as `[TRACE: relative_file_path.log]`) to recursively parse related log files.

However, the tool currently hangs and spins the CPU indefinitely when run against our production log set located in `/home/user/logs/`, specifically when starting with `/home/user/logs/master.log`.

Your tasks:
1. Identify why the tool is hanging. You should use system call tracing (e.g., `strace`) on the compiled binary to diagnose the runtime behavior and figure out which files are causing the issue.
2. Fix the bug in `/home/user/log-tracer/src/main.rs`. Modify the `count_errors` function (or related logic) so that it properly terminates and does not process the same log file more than once during a trace.
3. Write a regression test in `/home/user/log-tracer/src/main.rs` named `test_circular_trace`. This test must programmatically create a temporary circular log trace, run the `count_errors` function, and assert that it returns the correct error count without hanging.
4. After fixing the code, compile and run the binary against `/home/user/logs/master.log`.
5. Save the final integer output (the total number of errors) to `/home/user/error_count.txt`.

Ensure your regression test passes when `cargo test` is run in the `/home/user/log-tracer` directory.