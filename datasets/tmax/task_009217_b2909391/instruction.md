You are an engineer porting a C++ rate-limiting gRPC microservice to work inside a minimal Linux container. 

The service validates incoming requests using a proprietary shared library, `libvalidator.so`, and exposes a gRPC endpoint. You have been given the source code in `/home/user/app`, but the build is failing, and the tests are not passing.

Here is the situation:
1. When you run `make` in `/home/user/app`, the build fails with an `undefined reference` linker error related to `std::string` when building the `server`. The `libvalidator.so` library was compiled by an older compiler using the old C++11 ABI. You need to fix the `Makefile` to ensure `server.cpp` is compiled compatibly.
2. The `Makefile` also fails to configure the runtime library path (rpath). When the server starts, it cannot find `libvalidator.so`. You must fix the `Makefile` so the built `server` executable knows to look for shared libraries in `/home/user/app`.
3. After fixing the build, start the server (`./server`) in the background.
4. Run the provided `./client` executable to test the rate limiter. The client sends 5 consecutive requests to the server for the user "test_user". 
5. The rate limiter is configured to allow exactly 3 requests per user before blocking. Redirect the exact standard output of `./client` to `/home/user/test_results.log`.

**Requirements:**
- Do not modify `server.cpp`, `client.cpp`, or `libvalidator.cpp`. Only modify the `Makefile`.
- The final log file `/home/user/test_results.log` must contain the output of the client verifying the rate limiting behavior.