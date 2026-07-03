You are an integration developer working on a new "Video-to-API" emulator system. You need to deploy a C-based HTTP service that interprets instructions encoded in a video file and executes them based on URL parameters.

Your task consists of the following stages:

**1. Polyglot Build & Routing Header Generation**
There is a Rust project located at `/app/router_gen` that is supposed to read a configuration file (`/app/routes.json`) and generate a C header file (`router.h`) containing routing constants. However, the Rust project currently fails to compile due to lifetime issues.
Fix the Rust code so it compiles and runs successfully, OR rewrite the logic in a simple Python or C script. The goal is to generate a `router.h` file in `/home/user/` that correctly `#define`s the routes specified in the JSON. The primary route will be the execution endpoint.

**2. Video-based Interpreter Preparation**
There is a video file at `/app/signal.mp4` (resolution 100x100, 30 fps). This video encodes a sequence of bytecode instructions for a simple virtual machine.
Every exactly 1 second (at timestamps 0.0, 1.0, 2.0, etc.), the video displays a solid color for the entire frame. Each color corresponds to a VM instruction that modifies an integer accumulator:
*   Red (`#FF0000`): `INC` - Add 1 to the accumulator.
*   Green (`#00FF00`): `DEC` - Subtract 1 from the accumulator.
*   Blue (`#0000FF`): `MUL` - Multiply the accumulator by 2.
*   White (`#FFFFFF`): `RET` - Halt execution and return the accumulator value.

Extract these colors in sequence from the video to determine the exact program the VM needs to run. The program ends when the `RET` (White) instruction is encountered.

**3. C HTTP Server & Emulator**
Write a C program in `/home/user/server.c` that does the following:
*   Includes the generated `router.h`.
*   Starts a TCP HTTP server listening on `127.0.0.1:8080`.
*   Implements simple URL routing and parameter parsing. It must listen for HTTP GET requests matching the execution route (which should be `/api/exec`) with an `init` query parameter (e.g., `/api/exec?init=5`).
*   When a valid request is received, it initializes the accumulator with the integer value of `init`.
*   It then runs the extracted VM bytecode program on this accumulator.
*   Finally, it responds with an `HTTP/1.1 200 OK` status and the final integer value of the accumulator as plain text in the response body.
*   Any request to a non-matching route should return an `HTTP/1.1 404 Not Found`.

**Constraints & Deliverables:**
*   Compile your C server to `/home/user/server` and ensure it is running in the background listening on port 8080 before you finish.
*   Standard system tools (like `ffmpeg`, `gcc`, `rustc`, `cargo`, `python3`) are available.
*   The server must be robust enough to handle standard curl requests.