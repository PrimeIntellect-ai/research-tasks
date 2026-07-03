You are a mobile build engineer tasked with fixing and optimizing our distributed build cache pipeline. Our pipeline uses a Python gRPC service that wraps a core C++ shared library, but a recent update broke the ABI compatibility and the service configuration was lost. Furthermore, the build log processing script has become a severe bottleneck.

You need to complete the following multi-stage workflow:

1. **Architecture Configuration Retrieval (Image Fixture):**
   We have lost the original configuration file. However, the exact gRPC port to listen on and the strict rate-limiting threshold (requests per minute) are written in the architecture diagram located at `/app/build_arch.png`. You must read this image to extract these two integer values.

2. **ABI Fix and Shared Library Management:**
   The C++ shared library source code is in `/home/user/libmobilecore/`. A patch file `/home/user/libmobilecore/fix_abi.patch` has been provided to fix a recent struct layout change that broke the ABI. Apply this patch, recompile the shared library (`libmobilecore.so`), and ensure it is placed in `/home/user/libmobilecore/build/`.

3. **gRPC Service & Rate Limiting:**
   A protobuf definition exists at `/home/user/build_cache.proto`. Compile the Python gRPC stubs. Then, implement the Python gRPC server in `/home/user/server.py`. 
   - The server must implement the `BuildCache` service defined in the proto.
   - It must load and bind to the C++ shared library (`libmobilecore.so`) using `ctypes` to process cache keys.
   - It must listen on the exact port extracted from `/app/build_arch.png`.
   - It must implement request validation (reject empty cache keys) and an in-memory rate limiter that strictly enforces the limit (requests per minute) extracted from the image. Exceeding the limit should return a `RESOURCE_EXHAUSTED` gRPC status.

4. **Data Processing Optimization (Metric Threshold):**
   Our build pipeline generates massive diffs that need to be parsed. The current script `/home/user/diff_parser.py` works but is extremely slow. You must refactor and optimize `/home/user/diff_parser.py` so that it parses `/home/user/large_build.diff` significantly faster. The output format (a summary JSON written to `/home/user/diff_summary.json`) must remain exactly the same. An automated test will evaluate the execution speed of your optimized script against the original baseline. You need to achieve a speedup of at least 2.5x.

Leave the gRPC server running in the background and ensure all optimized scripts and compiled libraries are in their specified locations when you are finished.