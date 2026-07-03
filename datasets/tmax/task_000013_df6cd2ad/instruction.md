You are a web developer working on a Go web application located in `/home/user/webapp`. You have been given a patch file at `/home/user/thumbnail.patch` that adds a new `/thumbnail` endpoint to the server. This endpoint simulates processing images.

However, the patch is incomplete and buggy:
1. **Apply the patch:** Apply `/home/user/thumbnail.patch` to the repository in `/home/user/webapp`.
2. **Fix the build system (Conditional Builds):** The patch introduces OS-specific processing files (`proc_linux.go` and `proc_windows.go`). Currently, trying to build the project fails due to a redeclared function. You must fix the Go build tags so that `proc_linux.go` only compiles on Linux and `proc_windows.go` only compiles on Windows.
3. **Fix the memory leak:** The newly added `thumbnail.go` handler contains a severe memory leak. If you run a load test against the `/thumbnail` endpoint, the memory usage balloons infinitely. Identify and remove the cause of the memory leak in `thumbnail.go`.
4. **Cross-compile:** Once fixed, compile the application into two executable binaries and place them in `/home/user/webapp/build/`:
   - `/home/user/webapp/build/server_linux` (for Linux, `amd64`)
   - `/home/user/webapp/build/server_windows.exe` (for Windows, `amd64`)

Do not change the behavior of the `/thumbnail` endpoint other than fixing the memory leak (it should still return HTTP 200 and the correct string from the processor).