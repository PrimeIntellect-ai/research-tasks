I am trying to organize and fix a hybrid C and Rust project that has fallen into disrepair. The project is located at `/home/user/hybrid_project`. 

The project consists of a C shared library in `/home/user/hybrid_project/c_lib` that performs an algorithmic text transformation, and a Rust WebSocket server in `/home/user/hybrid_project/rust_server` that serves this C function over the network.

Right now, the project is broken:
1. The `Makefile` in the C library directory is misconfigured. It fails to compile the library as a proper shared object (`libtransform.so`) because it is missing the necessary Position Independent Code (PIC) flags and shared library flags.
2. I have created a patch file located at `/home/user/hybrid_project/c_lib/fix_makefile.patch` that should fix the `Makefile`. 

Your task is to:
1. Apply the patch `fix_makefile.patch` to the `Makefile` in the `c_lib` directory.
2. Compile the C shared library using `make`. It should produce `libtransform.so`.
3. Build the Rust WebSocket server using Cargo.
4. Run the Rust WebSocket server. Note: the Rust server relies on dynamically linking `libtransform.so` at runtime. You will need to ensure the system can find the shared library when starting the server (for example, by setting the appropriate environment variable). The server binds to `127.0.0.1:9001`.
5. Once the server is running, act as a WebSocket client and send the exact text message `"OrganizeFiles"` to the server at `ws://127.0.0.1:9001`.
6. Receive the transformed response string from the WebSocket server and save the exact response text to `/home/user/ws_response.txt`.

You may use any tool or language available in the environment to send the WebSocket message, as long as the final output is written to the specified file.