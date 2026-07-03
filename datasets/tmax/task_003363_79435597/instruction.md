You are an MLOps engineer responsible for deploying a lightweight, high-performance C++ inference service for tracking and sampling experiment artifacts. 

We have a vendored, proprietary C++ library located at `/app/bayesian_tracker-1.0.0/` which performs Bayesian updates and bootstrap sampling on artifact metric vectors using linear algebra routines. Unfortunately, a recent change introduced a bug: when missing data (represented as special sentinel integers) is ingested, the pipeline silently corrupts the integer state into floating-point NaNs due to an implicit cast in the matrix update step, causing downstream numerical accuracy tests to fail. Additionally, the provided `Makefile` in the vendored package has an incorrect environment variable reference for the compiler (`$CXX_COMPILER` instead of `CXX`), preventing it from building standardly.

Your task is to:
1. Fix the `Makefile` in `/app/bayesian_tracker-1.0.0/` so it uses the standard `CXX` variable and compiles correctly using `g++`.
2. Fix the numerical bug in `/app/bayesian_tracker-1.0.0/src/update_engine.cpp` where integer sentinel values (-9999) are incorrectly cast to floats and causing NaN propagation in the `bootstrap_update` function. The fix should explicitly ignore/drop the -9999 values before the matrix multiplication rather than casting them.
3. Write a C++ HTTP server using the (also provided) header-only `/app/httplib.h` that wraps this library.
4. The server must listen on `127.0.0.1:8080`.
5. The server must expose a `POST /sample` endpoint. The endpoint will receive a plaintext CSV payload of integers representing raw artifact metrics. 
6. The server must use the fixed `bayesian_tracker` library to compute the bootstrap posterior mean (using `Tracker::compute_mean`) and return it as a plain text float in the HTTP response body with an HTTP 200 status code.
7. If an incoming payload contains the `-9999` sentinel, the computation should successfully skip it (thanks to your fix) and return the correct numerical result without NaNs.
8. Start the server in the background and leave it running. Write a log file to `/home/user/server.log` that prints "Server started on port 8080".

Ensure your pipeline is reproducible and the server correctly responds to HTTP requests. Use only standard CLI tools and standard C++ libraries (plus the provided httplib).