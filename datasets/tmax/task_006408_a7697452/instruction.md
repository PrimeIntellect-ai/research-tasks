You are a systems programmer debugging a C library linking issue for a hybrid C/Rust application.

In `/home/user/matrix_app`, there is a Rust application `src/main.rs` that exposes a simple TCP server. It binds to a C shared library to perform matrix computations. However, the system is currently broken in multiple ways:
1. The Rust code has a borrow checker error and fails to compile.
2. The deployment directory `/home/user/matrix_app/libs` contains three versions of the shared library (`libcompute_v1.so`, `libcompute_v2.so`, and `libcompute_v3.so`). Due to an ABI requirement, the Rust FFI strictly requires the `compute_matrix` function to have an exact mathematical compiled size of 128 bytes (0x80 in hex).
3. The application needs to be exposed via a reverse proxy on port 9090, but the Rust server hardcodes its listener to port 8000.

Your task is to write a deployment Bash script at `/home/user/matrix_app/deploy.sh` that performs the following steps when executed:

1. Fixes the Rust ownership error in `/home/user/matrix_app/src/main.rs`. (You may use standard utilities like `sed` in your script to patch it, or fix it manually before running the script—but the script must successfully compile the Rust code).
2. Compiles the Rust application using `rustc`: 
   `rustc -L /home/user/matrix_app/libs src/main.rs -o server`
3. Inspects the `.so` files in `/home/user/matrix_app/libs/` using standard binary analysis tools (like `nm`, `readelf`, or `objdump`) to find the one where the `compute_matrix` symbol's size is exactly 128 bytes.
4. Creates a symlink `/home/user/matrix_app/libs/libcompute.so` pointing to the correct version.
5. Writes the filename of the correct library (e.g., `libcompute_v1.so`) to `/home/user/matrix_app/abi_version.txt`.
6. Starts the compiled `./server` in the background, ensuring the dynamic linker can find the shared library (e.g., using `LD_LIBRARY_PATH`).
7. Starts a reverse proxy using `socat` that listens on TCP port 9090 and forwards traffic to the Rust server on `127.0.0.1:8000`. Run this in the background as well.

The script must be executable (`chmod +x`). 

Verify your deployment by ensuring that running `./deploy.sh` completes without errors, and that you can successfully receive a response by running `curl http://127.0.0.1:9090`.