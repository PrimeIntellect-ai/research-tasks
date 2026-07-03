I am a systems programmer working on a new service, and I'm currently stuck debugging a C library linking issue within a Go application. 

My Go application (`/home/user/project/src/main.go`) acts as a WebSocket server and uses `cgo` to interface with a proprietary C library (`libsolver.so`) that performs complex constraint satisfaction logic.

However, the project is currently broken in two ways:
1. **Linking Issue**: When I run `go build`, it fails to link against `libsolver.so`. The C headers and the compiled shared library are located in `/home/user/project/lib`. You need to fix the `cgo` directives in `main.go` so that the Go compiler can find the library at compile-time, and the resulting binary can find it at run-time without needing to manually set `LD_LIBRARY_PATH`.
2. **Concurrency Bug**: There is a custom data structure in `/home/user/project/src/hub.go` that manages connected WebSocket clients. When multiple clients connect and disconnect simultaneously, the program panics with a "concurrent map read and map write" error. You need to implement proper Go concurrency patterns (e.g., using `sync.Mutex` or `sync.RWMutex`) to make the `Hub` data structure thread-safe.

Your task:
1. Fix the `cgo` linking issue in `main.go`.
2. Fix the data race in `hub.go`.
3. Compile the final, working executable to exactly `/home/user/project/bin/server`.

You can test your work by running the server and connecting to it via websockets on port `8080`. Send the text `"solve 5"` and it should broadcast the result `"solved: 25"` to all connected clients.