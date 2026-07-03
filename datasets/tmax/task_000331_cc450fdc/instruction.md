You are a QA engineer setting up a test environment for a new C-based mathematical API. 

We have the source code for a URL evaluation engine, but it hasn't been compiled or rigorously tested. Your objective is to build the shared library, write a test harness, generate property-based test cases to verify the commutative property of addition, and log the sorted results.

You are provided with two files that already exist on the system:
1. `/home/user/math_api.h`
2. `/home/user/math_api.c`

Here are your instructions:
1. **Shared Library Management**: Compile `/home/user/math_api.c` into a shared library named `/home/user/libmathapi.so`.
2. **Test Harness**: Write a C program at `/home/user/test_harness.c` that dynamically links against `libmathapi.so` (or uses standard linking if the library is in the library path). The harness must:
   - Read URLs from standard input line by line (up to 256 characters per line).
   - Pass each URL to the library function: `int evaluate_url(const char* url, double* out_val);`
   - Print the result to standard output in the exact format: `<url> = <val>` where `<val>` is a floating-point number formatted to exactly 2 decimal places. (e.g., `/api/add?a=5&b=3 = 8.00`). If `evaluate_url` returns a non-zero error code, print `<url> = ERROR`.
3. **Property-Based Test Generation**: Write a bash script at `/home/user/generate_urls.sh` that generates exactly 20 test URLs to stdout. These URLs must test the commutative property of addition for the integers 1 through 10. 
   Specifically, for each integer $i$ from 1 to 10, output two URLs on separate lines:
   - `/api/add?a=X&b=Y`
   - `/api/add?a=Y&b=X`
   where `X` is $i$ and `Y` is $i \times 2$.
4. **Execution and Sorting**: Compile your test harness to `/home/user/test_harness`. Run `generate_urls.sh`, pipe its output into `test_harness`, sort the resulting output lines alphabetically, and redirect the final sorted output to `/home/user/sorted_results.log`.

Do not hardcode the results; the harness must actively call the compiled shared library.