You are a release manager preparing a deployment for a critical legacy mathematical microservice. 

A proprietary, closed-source mathematical core was provided by a vendor as a stripped ELF shared library located at `/app/liblegacy_math.so`. The documentation for this library has been lost. We only know the following:
1. It exports a single dynamic symbol (a mathematical function).
2. The function computes a custom "zeta" transformation.
3. The function signature takes an integer `iterations` and a double-precision float `value`, and returns a double-precision float result.

Your goal is to wrap this library in a REST API microservice using C.

We have provisioned a workspace in `/home/user/` with the following files:
- `/home/user/vendor/mongoose.c` and `/home/user/vendor/mongoose.h`: A lightweight web server framework.
- `/home/user/server.c`: An incomplete C source file for the API.
- `/home/user/Makefile`: A broken Makefile that fails to build the application.

Task Requirements:
1. **Discover the ABI**: Inspect `/app/liblegacy_math.so` to find the exact name of the exported mathematical function.
2. **Complete the API**: Edit `/home/user/server.c` so that it uses the Mongoose web server to listen on `127.0.0.1:9090`. 
   - It must expose a `GET /zeta` endpoint.
   - It must accept query parameters `iter` (integer) and `val` (double).
   - It must invoke the function from the legacy shared library.
   - It must return a JSON response in the exact format: `{"result": 123.456}` (where 123.456 is the returned double).
3. **Fix the Build**: Modify `/home/user/Makefile` so that `make` successfully compiles `/home/user/server.c` into an executable at `/home/user/server`. Ensure that the library `/app/liblegacy_math.so` is properly linked and the resulting binary can execute without manually setting `LD_LIBRARY_PATH`.
4. **Deploy**: Start the server process in the background so it is ready to accept requests.

Constraints:
- Do not modify the legacy binary.
- Do not use root privileges; compile and run locally.
- Keep the server running on `127.0.0.1:9090` at the end of your workflow.