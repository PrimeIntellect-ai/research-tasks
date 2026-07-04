You are a systems programmer tasked with deploying a secure web-facing sandbox. The sandbox is a custom bytecode emulator written in Rust, which interfaces with a legacy C library for cryptographic operations. 

Currently, the project is in a broken state at `/home/user/project/`. You need to fix it, configure a reverse proxy, and verify it works.

Here are your specific objectives:

1. **Fix C Library Linking**: 
   The C library is located in `/home/user/project/c_lib/`. It consists of `crypto_dummy.c` and `crypto_dummy.h`. Compile this into a shared object `libcrypto_dummy.so`. 
   The Rust emulator in `/home/user/project/emulator/` uses FFI to call this library, but it currently fails to link. Fix the configuration (e.g., `build.rs` or environment variables) so that `cargo build` succeeds.

2. **Fix Rust Borrow Checker Error**:
   The Rust emulator has a borrow checker error in `/home/user/project/emulator/src/main.rs` within the interpreter loop. You must debug and fix this ownership/borrowing issue without changing the core logic of the emulator.

3. **Configure Reverse Proxy**:
   Create an Nginx configuration file at `/home/user/project/nginx.conf`. It must:
   - Run entirely in user-space (no root required; use `/home/user/project/nginx_temp/` for pid and logs).
   - Listen on port 8080.
   - Proxy all requests to the Rust emulator, which binds to `127.0.0.1:9000`.
   - Add a security response header: `X-Sandbox-Secure: true`.

4. **Verify**:
   Once the Rust emulator and Nginx reverse proxy are both running, send a `curl -i` request to `http://127.0.0.1:8080/run?code=1` and save the complete output (including headers) to `/home/user/success.log`.