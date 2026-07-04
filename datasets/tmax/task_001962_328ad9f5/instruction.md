You are tasked with porting and optimizing a legacy audio processing tool into a containerized REST microservice. The system consists of a multi-language pipeline:

1. **WAV Parser (Rust):** Located in `/app/wav_parser/`. It's supposed to expose a C-compatible ABI to parse WAV headers, but currently fails to compile due to a lifetime/borrow checker error in `src/lib.rs`.
2. **Audio Filter (C):** Located in `/app/c_filter/`. It implements a naive moving average filter for audio signals. The `Makefile` is currently broken and fails to build the shared library `libfilter.so` due to missing position-independent code flags and incorrect linker rules.
3. **Core Logic (C++):** Located in `/app/cpp_core/`. You need to write a C++ shared library (`libcore.so`) that uses FFI to call the Rust WAV parser and the C Audio Filter. The C filter algorithm is currently $O(N \times K)$ where $K$ is the window size. You must rewrite/optimize the C++ wrapper or the C core to implement the moving average filter in $O(N)$ time (e.g., using a sliding sum or vectorization).
4. **REST API (Python):** Located in `/app/api/server.py`. It uses `ctypes` to load `libcore.so`. You must implement a REST endpoint `POST /process` using FastAPI or Flask that accepts a file path. You must also implement **strict rate limiting**: no more than 5 requests per minute per IP address (return HTTP 429 Too Many Requests).

**Testing / Input:**
There is a 3-minute WAV file located at `/app/fixture_audio.wav`.
The moving average window size is strictly `1000` samples.

**Your objectives:**
1. Fix the Rust borrow checker issue and compile `libwav_parser.so`.
2. Fix the C `Makefile` and compile `libfilter.so`.
3. Write the C++ FFI integration, optimize the algorithm to run significantly faster than the naive baseline, and compile it to `libcore.so`.
4. Add rate limiting to the Python REST API and ensure it successfully returns the processed audio array.
5. Create a shell script `/app/run_server.sh` that starts the API on port `8000`.

The automated verifier will start your server, send requests to process `/app/fixture_audio.wav`, check the accuracy of the output (Mean Squared Error), test the rate limiter, and measure the processing latency.