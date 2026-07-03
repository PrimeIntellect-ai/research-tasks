You are tasked with setting up and fixing a polyglot build system and computation engine from scratch. The system consists of a high-performance Rust computation core and a Python-based API wrapper.

Here is the current state of the workspace:
- A specification for the numerical algorithm has been provided as an image at `/app/algorithm_spec.png`.
- The scaffolding for the Rust computation core is located at `/home/user/polyglot/compute_engine/`. Unfortunately, the previous engineer left it with borrow-checker errors and a dummy implementation.

Your objectives are:

1. **Algorithm Recovery**: Read the mathematical specification from `/app/algorithm_spec.png` (you may use `tesseract` to extract the text).
2. **Rust Core Implementation**: 
   - Fix the Rust ownership/borrowing errors in `/home/user/polyglot/compute_engine/src/main.rs`.
   - Implement the exact numerical algorithm described in the image.
   - The compiled binary must accept a single non-negative integer argument `N` from the command line and print ONLY the computed integer result to standard output.
   - You must build the release version of the binary. The final executable must be located at `/home/user/polyglot/compute_engine/target/release/compute_engine`.
3. **API Setup**:
   - Create a Python FastAPI application at `/home/user/polyglot/api/server.py`.
   - It should expose a `GET /compute?n=<integer>` endpoint that invokes your Rust binary and returns `{"result": <computed_value>}`.
   - Implement rate limiting on this endpoint (maximum 5 requests per minute per IP address). Return a 429 status code if the limit is exceeded. 
   - Write a `Makefile` at `/home/user/polyglot/Makefile` that has two targets: `build` (which compiles the Rust binary) and `run-api` (which starts the Python server on port 8000).

Ensure your Rust binary is perfectly accurate and robust. Automated integration tests will perform strict fuzz-testing against your compiled Rust binary using thousands of random inputs to verify mathematical equivalence with a reference oracle.