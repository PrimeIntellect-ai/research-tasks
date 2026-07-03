You are acting as a systems programmer to deploy a high-performance checksumming web service. You have been provided with a vendored C library for fast checksum calculation and must integrate it into a C++ backend behind a configured reverse proxy.

Your workspace is located at `/app/`.
Inside `/app/`, you will find:
1. `libfastcrc-1.2/` - A vendored C library containing `fastcrc.h`, `fastcrc.c`, and a `Makefile`.
2. `httplib.h` - A single-file C++ HTTP server library (cpp-httplib).

Perform the following steps:

1. **Fix and Compile the C Library**
   The `Makefile` inside `libfastcrc-1.2/` is broken. It fails to correctly generate a dynamically linkable shared library (`libfastcrc.so`) and uses poor optimization flags. 
   Fix the `Makefile` so it properly builds a shared library `libfastcrc.so`. You **must** enable high optimizations (e.g., `-O3`) because the verifier will measure the performance of your service against a strict latency threshold.

2. **Develop the C++ HTTP Backend**
   Write a C++ HTTP server at `/app/server.cpp` using the provided `httplib.h`.
   - The server must listen on `127.0.0.1` port `9000`.
   - Expose a `POST /checksum` endpoint.
   - The endpoint should read the request body, compute its CRC32C checksum using the `compute_crc32c(const unsigned char* data, size_t length)` function provided by `libfastcrc.so`, and return the integer checksum as a plain text response (e.g., "12345678").
   - Link the C++ server dynamically against `libfastcrc.so`.

3. **Configure Nginx Reverse Proxy**
   Write an Nginx configuration file at `/app/nginx.conf` that sets up a reverse proxy for your C++ backend.
   - Listen on `0.0.0.0` port `8080`.
   - Forward requests to `127.0.0.1:9000`.
   - Enforce request validation: only allow `POST` requests to `/checksum`. Other methods should return a `405 Method Not Allowed`.
   - Enforce rate limiting: configure a rate limit of exactly `100 requests per second` per client IP (using Nginx's `limit_req_zone` and `limit_req`). Use a zone name `req_limit_per_ip` with a size of `10m`.
   - Limit the client body size to exactly `5M`.

4. **Automation Script**
   Create a bash script at `/app/start.sh` that:
   - Recompiles the C library.
   - Compiles the C++ server.
   - Starts the C++ backend in the background.
   - Starts Nginx using your custom configuration.
   Ensure all file paths and library paths are correctly configured so the backend doesn't crash on startup due to missing `.so` files.

The automated verifier will execute your `/app/start.sh` script, wait for the services to become ready, and then run a benchmark suite. The benchmark will evaluate correctness, test the Nginx rate limiting, and calculate the average latency to checksum 1MB payloads. To pass, the measured average latency must be strictly less than a targeted metric threshold, which requires fixing the C library's build process.