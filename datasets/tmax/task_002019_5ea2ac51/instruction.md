You are an engineer tasked with setting up a polyglot build system from scratch using Bash. We have a multi-tier application consisting of a backend C server and a Go reverse proxy. The source code has some issues, and the build process needs to be completely automated.

Your goal is to write a single Bash script at `/home/user/build.sh` that automatically repairs the codebase, builds the binaries, starts the services, and verifies they are working correctly. 

The workspace is located at `/home/user/polyglot-build/` and contains two directories:
1. `c_src/`: Contains a backend HTTP server written in C (`main.c`) and a broken Makefile (`Makefile.broken`).
2. `go_src/`: Contains a Go reverse proxy (`proxy.go`) that utilizes goroutines, and a patch file (`proxy_fix.patch`).

Your script `/home/user/build.sh` must perform the following actions:
1. **Makefile Repair:** The file `c_src/Makefile.broken` uses 4 spaces for indentation instead of tabs, which breaks `make`. Read this file, replace all leading 4-space indentations with a single tab character, and save it as `c_src/Makefile`.
2. **C Compilation:** Run `make` inside the `c_src/` directory to compile the C program. This will produce a binary named `c_server`.
3. **Diff and Patch Processing:** The `go_src/proxy.go` file has a bug. Apply the patch `go_src/proxy_fix.patch` to fix it.
4. **Go Compilation:** Compile the Go reverse proxy by running `go build -o proxy_server proxy.go` inside the `go_src/` directory.
5. **Service Orchestration:** 
   - Start the C backend server (`./c_src/c_server`) in the background. It will bind to port 8081.
   - Start the Go reverse proxy (`./go_src/proxy_server`) in the background. It will bind to port 8080 and forward requests to 8081.
   - Ensure your script gives the servers a second to start up (e.g., `sleep 2`).
6. **API Verification:** Make a GET request using `curl` to the reverse proxy at `http://127.0.0.1:8080/api/status`. The Go reverse proxy adds a custom `X-Proxy-Version` header before hitting the C server. 
7. **Logging:** Save the raw body response of the `curl` command directly into `/home/user/build_result.log`.

Make sure your script `/home/user/build.sh` is executable (`chmod +x`). Do not run the script yourself; the automated testing suite will execute `/home/user/build.sh` and verify the contents of `/home/user/build_result.log` and the system state.