You are helping a developer fix and organize a mixed Go and C project that calculates large Fibonacci numbers modulo 1000000007 concurrently. The project files are located in `/home/user/math_project`.

The project structure is intended to be:
`/home/user/math_project/`
├── `include/fib.h`       (C Header)
├── `src/fib.c`           (C Implementation)
├── `lib/`                (Directory for the compiled shared library, currently empty)
├── `Makefile`            (Build script for the C library)
└── `main.go`             (Go application that uses CGO and goroutines)

Currently, the project is broken:
1. The `Makefile` has missing compilation flags for creating a shared library (`-fPIC`, `-shared`) and uses spaces instead of tabs. It also fails to place the output correctly in the `lib` directory.
2. The `main.go` file has incorrect `#cgo` directives pointing to non-existent `wrong_include` and `wrong_lib` directories instead of the proper `include` and `lib` directories.

Your task is to:
1. Fix the `Makefile` so that running `make` inside `/home/user/math_project` successfully builds `libfib.so` and places it inside `/home/user/math_project/lib/`.
2. Fix the `#cgo` directives in `/home/user/math_project/main.go` to point to the correct `include` and `lib` directories.
3. Build and run the Go application. Before running the Go application, you may need to set the `LD_LIBRARY_PATH` environment variable so it can find `libfib.so` at runtime.
4. The Go program is already written to spawn goroutines, calculate results, and write the final sum to `/home/user/result.txt`. Ensure this file is generated successfully.