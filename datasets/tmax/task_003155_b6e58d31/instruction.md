You are a systems programmer tasked with rescuing a partially migrated legacy system. A critical component that computes a proprietary checksum for data payloads was originally written in C. We are migrating this to a Rust-based gRPC service, but the original C source code and headers have been lost.

You have been provided with:
1. A stripped compiled shared library at `/app/libcustom_crc.so`.
2. A broken Rust project at `/home/user/crc_service`.
3. An Nginx reverse proxy template directory at `/home/user/proxy`.

Your objectives:

1. **Assembly Analysis & FFI Fix:** 
   The Rust project currently fails to run or produces segmentation faults when calling the C library because the FFI bindings in `/home/user/crc_service/src/crc_ffi.rs` are incorrect. You must analyze the stripped binary (`/app/libcustom_crc.so`), determine the correct signature and calling convention for the exported hashing function (hint: it's named `calculate_crc`), and fix the Rust FFI bindings.

2. **gRPC Service Implementation:**
   Implement a gRPC server in `/home/user/crc_service` using the `tonic` crate. You need to write the `proto/crc.proto` file with a service `CrcService` containing an RPC `ComputeCrc` that takes a `CrcRequest` (containing `bytes data` and `uint32 initial_value`) and returns a `CrcResponse` (containing `uint32 checksum`). The server must run on `127.0.0.1:50051`.

3. **Reverse Proxy Configuration:**
   Configure Nginx as an HTTP/2 reverse proxy listening on port `8080`. It must route gRPC requests to your Rust service on `50051`. Write your Nginx configuration to `/home/user/proxy/nginx.conf` and ensure Nginx is started using this config.

Once you are done, leave the Rust gRPC server running in the background, and Nginx running using your configuration. The automated verification will test the gRPC endpoint on port `8080` by sending a batch of random payloads.