You are an engineer tasked with recovering a lost polyglot CI/CD pipeline configuration and exposing a build service. 

We have a corrupted telemetry video from our build server, located at `/app/telemetry.mp4`. This video is essentially a sequence of solid black and white frames flashing at 1 frame per second.
A black frame represents a `0` and a white frame represents a `1`. 
The binary sequence encoded in this video, read from start to finish, defines a mathematical constraint satisfaction problem that determines the exact versions of our tools (Python, Node, and Go) needed for our build system.

The binary sequence is structured as follows:
- The first 12 bits represent an integer `A`.
- The next 12 bits represent an integer `B`.
- The next 12 bits represent an integer `C`.
(All integers are unsigned, big-endian).

Our system has three dependency versions we need to resolve: `X` (Python minor version 3.X), `Y` (Node major version Y), and `Z` (Go minor version 1.Z).
They must satisfy the following constraints:
1. `X + Y + Z = A`
2. `X * Y + Z = B`
3. `X^2 + Y^2 - Z = C`
4. `X`, `Y`, and `Z` are all positive integers between 1 and 30.

Your objective is to:
1. Extract the frames from `/app/telemetry.mp4` (you may use `ffmpeg`) and decode the binary sequence to find `A`, `B`, and `C`.
2. Write a Go program that concurrently searches the solution space (using goroutines and channels) to find the unique combination of `X`, `Y`, and `Z` that satisfies the constraints.
3. Build a polyglot build service in Go that exposes:
   - An HTTP server on `0.0.0.0:8080`. A `GET /versions` request should return a JSON response exactly like: `{"python": "3.X", "node": "Y", "go": "1.Z"}`.
   - A TCP server on `0.0.0.0:9000`. When it receives the string `BUILD\n`, it should execute a dummy build script `/home/user/build.sh` (you need to create a simple bash script that just `echo "Building with Python 3.X, Node Y, Go 1.Z"` and exits with 0) and respond to the TCP client with `SUCCESS\n`.

Ensure your Go service is robust, includes a basic test fixture for the constraint solver, and is left running in the background. Write your Go code in `/home/user/workspace/`.