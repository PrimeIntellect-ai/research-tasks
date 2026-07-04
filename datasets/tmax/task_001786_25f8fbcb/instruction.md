You are an engineer setting up a build system and an execution server for a polyglot application. We are embedding Lua into a C++ service, but the build environment needs fixing.

We have pre-vendored the source code of Lua 5.4.6 in `/app/vendored/lua-5.4.6`. Unfortunately, a recent automated refactoring script introduced a bug into its Makefile, and it currently fails to compile on Linux.

Your objectives:
1. **Fix the Vendored Package:** Diagnose and fix the build error in `/app/vendored/lua-5.4.6/src/Makefile`. Once fixed, build the Lua static library (`liblua.a`) by running `make linux` in the root of the Lua source directory.
2. **Implement the Server:** In `/home/user/workspace`, write a C++ program named `server.cpp`. This program must embed the built Lua library and act as a raw TCP server listening on `127.0.0.1:8888`.
3. **Protocol Details:** 
   - When a client connects via TCP, the server should read exactly one line of text (up to and including `\n`).
   - The received line will be a valid Lua expression that returns a number (e.g., `return 10 * 2.5`).
   - The C++ server must evaluate this expression using the embedded Lua C API.
   - The server must send the numeric result back to the client as a string followed by a newline (`\n`), and then close the connection.
4. **Build System:** Create a `Makefile` in `/home/user/workspace` that compiles `server.cpp` using `g++` and links it against the vendored `/app/vendored/lua-5.4.6/src/liblua.a`. Ensure the `-ldl` and `-lm` flags are included if necessary. The compiled executable must be named `lua_server`.
5. **Execution:** Build the `lua_server` and run it in the background so it is actively listening on port 8888 when you complete your task.

Make sure your C++ server gracefully handles multiple sequential connections (it does not need to handle concurrent connections). Leave the `lua_server` running when you finish.