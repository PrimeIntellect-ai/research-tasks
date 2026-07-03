You are tasked with fixing and completing a custom esoteric language interpreter written in Go, specifically designed for data processing tasks. The project is located at `/home/user/interp`.

Currently, the project fails to compile due to broken build tags and incomplete data structures. 

Here is what you need to do:

1. **Fix Build System and Cross-Compilation:**
   The project has OS-specific files (`tape_linux.go` and `tape_windows.go`) that currently have conflicting or incorrect Go build constraints (build tags). Fix them so that they correctly compile *only* for their respective operating systems (`linux` and `windows`). Use modern Go build tag syntax (`//go:build ...`). 

2. **Implement Custom Data Structure:**
   In `tape.go`, the `Tape` interface is defined, but the `RingTape` struct is incomplete. Implement `RingTape` to act as a 256-byte circular buffer (wrapping around at the edges: moving left from index 0 goes to 255, moving right from 255 goes to 0). It must implement the `Tape` interface (`MoveLeft()`, `MoveRight()`, `Inc()`, `Dec()`, `Read() byte`, `Write(byte)`). 
   Update `NewRingTape()` to return an initialized `RingTape`.

3. **Performance Benchmarking:**
   Create a benchmark in `tape_test.go` called `BenchmarkTape` that benchmarks the `Inc()` and `MoveRight()` operations of your `RingTape` (e.g., inside the benchmark loop `b.N`, call `Inc()` and `MoveRight()`). 
   Run this benchmark using `go test -bench .` and save the exact console output to `/home/user/interp/bench.txt`.

4. **Build and Process Data:**
   Use the provided `Makefile` to compile the Linux binary (`make build-linux`).
   The resulting binary will be named `interp-linux`.
   Run the interpreter on the provided data script `/home/user/interp/input.df`. Redirect the standard output of the interpreter to `/home/user/interp/output.dat`.
   
   Example usage of the binary: `./interp-linux < /home/user/interp/input.df > /home/user/interp/output.dat`

The task is considered successful when `make build-linux` and `make build-windows` succeed, `bench.txt` contains the benchmark output, and `output.dat` contains the correct evaluated output of the `input.df` script.