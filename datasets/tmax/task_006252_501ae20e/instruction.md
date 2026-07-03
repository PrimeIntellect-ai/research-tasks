You are a platform engineer maintaining a CI/CD pipeline for a custom networking appliance. The team has developed a fast C++ URL routing and parameter parsing library (`url_router`), which includes a custom checksum validation for incoming requests. 

However, the pipeline is currently broken. The project is located at `/home/user/url_router/`. 

Your objectives are:
1. **Fix the Build**: The `Makefile` has a linking error preventing the `router_test` and `router_app` targets from building. Fix the `Makefile` so that running `make all` successfully builds both executables.
2. **Find and Fix the Bug**: There is a bug in the URL parameter parsing logic in `router.cpp` that causes a crash or incorrect behavior on certain malformed or edge-case query strings. 
   - Implement a custom property-based fuzzing test in `test.cpp` that generates random URL query strings (e.g., varying lengths, missing values, empty keys) to test the `Router::parse` function.
   - Run the test to identify the bug.
   - Fix the bug in `router.cpp` so that it handles all valid and edge-case URLs without crashing, correctly assigning empty strings to parameters missing values (e.g., `?key=&other=1` should yield `key`="", `other`="1").
3. **Performance Benchmarking**: The team needs to ensure the parser is fast. Add a command-line argument `bench` to `main.cpp`. When `./router_app bench` is executed, it should:
   - Run the `Router::parse` function 100,000 times on the URL: `/api/v1/data?id=999&checksum=a1b2&flags=active&mode=`
   - Measure the total elapsed time for these 100,000 iterations.
   - Write ONLY the elapsed time in milliseconds (as a simple integer or float, e.g., `42`) to `/home/user/benchmark.log`.

Requirements for `/home/user/benchmark.log`:
- It must contain only the numeric value of the benchmark duration in milliseconds.

Ensure all code compiles with `-std=c++17` and no memory leaks or crashes occur during the execution of your test and benchmark.