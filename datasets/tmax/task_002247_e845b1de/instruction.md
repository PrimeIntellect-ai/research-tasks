You are a script developer tasked with porting a slow Python mathematical utility to a high-performance Go implementation using an existing highly optimized x86-64 assembly routine. 

Your workspace is located at `/home/user/math_util`. 

The directory contains the following files:
1. `/home/user/math_util/ref.py`: A Python script containing the reference mathematical sequence calculation.
2. `/home/user/math_util/fast_math.s`: An x86-64 System V AMD64 ABI assembly file exporting the function `fast_mult(a, b, m)` which computes `(a * b) % m`.
3. `/home/user/math_util/fast_math.h`: The C header file declaring `uint64_t fast_mult(uint64_t a, uint64_t b, uint64_t m);`.

Your objectives are:
1. **Translate the Python logic into Go**: Create `/home/user/math_util/main.go` that perfectly replicates the logic in `ref.py`. 
2. **Integrate Assembly via CGO**: In your Go code, you must replace the modular multiplication step `(seed * i) % m` with a call to the C function `fast_mult` via `cgo`. 
3. **Polyglot Build Orchestration**: Write a bash script `/home/user/math_util/build.sh` that:
   - Uses `gcc` to assemble `fast_math.s` into an object file `fast_math.o` or directly links it during the Go build.
   - Compiles the Go code into a final executable named `/home/user/math_util/math_runner`. (Ensure your CGO directives are properly set up to link against the assembly).
   - The build script must be executable.
4. **Execution**: Run your build script, then execute `./math_runner` and redirect its standard output to `/home/user/math_util/result.txt`.

The final file `/home/user/math_util/result.txt` must contain only the final integer calculated by the Go program.