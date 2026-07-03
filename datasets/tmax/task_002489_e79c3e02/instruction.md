I'm trying to organize a mixed-language project located in `/home/user/project`, but I've run into linking errors, memory corruption crashes, and I haven't finished the Go concurrency wrapper. 

Right now, all my files (`Makefile`, `lib.c`, `lib.h`, `main.go`) are dumped in the root directory. 

I need you to fix the code and organize the project into the following structure:
- `/home/user/project/src/` : Should contain `lib.c`, `lib.h`, and a new assembly file `magic.s`.
- `/home/user/project/cmd/` : Should contain `main.go`.
- `/home/user/project/lib/` : Should contain the compiled shared library `libmyc.so`.
- `/home/user/project/bin/` : Should contain the compiled Go binary `app`.

Here are the specific fixes required:
1. **Assembly Component:** The C code calls an external function `int get_magic();`. Write a minimal x86_64 Linux assembly implementation in `magic.s` that simply returns the integer `5`.
2. **C Memory Bug:** `lib.c` has an undefined behavior / out-of-bounds memory access issue. Find and fix it so it doesn't crash or read garbage memory.
3. **Makefile:** Update the Makefile to compile `lib.c` and `magic.s` into a shared library `libmyc.so` inside the `lib/` directory.
4. **Go Concurrency:** Update `main.go` to import the C library using `cgo`. It must run the `process()` function from the C library concurrently using **exactly 15 goroutines**. Sum the results from all 15 goroutines and write the final total integer to `/home/user/project/output.txt`. 
5. Compile the Go program and place the executable at `/home/user/project/bin/app`. Run your Go binary once to generate `output.txt`.

Ensure your Go application safely manages the concurrent calls (using sync primitives) and that the C library is safe to call concurrently.