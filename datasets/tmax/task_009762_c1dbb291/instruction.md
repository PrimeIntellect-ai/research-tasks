You are acting as a release manager preparing a new deployment for our custom bytecode processing tool. The deployment pipeline is failing. 

We have a Go project in `/home/user/release/go-emu` that wraps a custom C-based emulator library located in `/home/user/release/libemu`. 

Currently, the build and execution pipeline fails due to two issues:
1. The C library's Makefile (`/home/user/release/libemu/Makefile`) is broken. It throws a structural error when `make` is run.
2. The Go wrapper (`/home/user/release/go-emu/main.go`) contains a state machine bug. It reads hex-encoded custom bytecode from `/home/user/release/payload.hex`, decodes it, and processes it via the C library. However, the parser's state machine gets stuck in the `STATE_READING` state when it encounters the `0xEE` (Escape) byte, causing an infinite loop or incorrect output.

Your task:
1. Fix the `Makefile` in `/home/user/release/libemu` so that it successfully compiles `libemu.a`.
2. Fix the state machine bug in `/home/user/release/go-emu/main.go` so it correctly transitions to `STATE_ESCAPED` when encountering `0xEE`, processes the next byte literally without evaluating it as a command, and then returns to `STATE_READING`.
3. Build the Go application.
4. Run the Go application with the input file `/home/user/release/payload.hex`.
5. Save the standard output of the Go application to `/home/user/release/manifest.log`.

The output in `manifest.log` must be the exact sequence of processed integer results separated by spaces.