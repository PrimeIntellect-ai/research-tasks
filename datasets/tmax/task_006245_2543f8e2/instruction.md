You are an engineer tasked with investigating a crashing and leaking long-running mathematical service. The service, located at `/home/user/poly_service/`, evaluates polynomials from a continuous data stream. However, the current code fails to build, crashes on certain inputs, and has a severe memory leak.

Here is the current state of the project:
- `/home/user/poly_service/Makefile`: Builds the project.
- `/home/user/poly_service/poly_eval.cpp`: The main service code.
- `/home/user/poly_service/fastmath.cpp` and `fastmath.h`: A custom math library used by the service.
- `/home/user/poly_service/input.txt`: A test file containing sample stream data.

Your objectives:
1. **Fix the build environment**: The `Makefile` has a missing linkage step causing a linker error (`undefined reference to fast_pow`). Fix the Makefile so `make` successfully compiles `poly_eval`.
2. **Fix format parsing edge-cases**: The string parsing logic in `poly_eval.cpp` cuts off the last character of the coefficients string when there isn't a trailing space before the `| X:` delimiter. Fix the string boundaries.
3. **Fix boundary conditions**: The polynomial degree array allocation and loop bounds have off-by-one errors leading to memory corruption. A polynomial of degree $N$ requires $N+1$ coefficients.
4. **Fix the memory leak**: The application leaks memory on every parsed line. Ensure no memory is leaked (you can test with `valgrind`).
5. **Generate Output**: Once fully patched, run the compiled `./poly_eval` binary. It will automatically read `input.txt`. Redirect the standard output to `/home/user/poly_service/output.log`.

The final `/home/user/poly_service/output.log` must contain exactly the evaluated numerical results, one per line. Do not print anything else to standard output.