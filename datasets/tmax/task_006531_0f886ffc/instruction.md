You are an integration developer. Your task is to build a mathematical web API in Rust from scratch and create an end-to-end (E2E) test orchestration script to verify its correctness. 

Please complete the following phases:

**Phase 1: The Rust Mathematical API**
Create a new Rust project at `/home/user/math_api`. Write a web service (using a framework of your choice, like `axum`, `actix-web`, or `warp`) that listens on `127.0.0.1:8123` and provides the following two endpoints:

1. **GET `/collatz/:n`**
   - Parses the unsigned 64-bit integer `n` from the URL parameter.
   - Computes the length of the Collatz conjecture sequence starting at `n`. (The sequence ends when it reaches 1. The starting number counts as step 0, e.g., for `n=1`, length is 0; for `n=2`, length is 1).
   - Returns a JSON response in the format: `{"n": n, "length": L}` where `L` is the computed length.

2. **POST `/determinant`**
   - Accepts a JSON body containing an NxN matrix of 64-bit floats: `{"matrix": [[...], ...]}`.
   - Implements a numerical algorithm to compute the determinant of the provided square matrix.
   - Returns a JSON response: `{"determinant": D}`.

**Phase 2: End-to-End Test Orchestration**
Create a bash script at `/home/user/run_e2e.sh` that acts as a mini CI/CD pipeline. The script must:
1. Compile the Rust API project in release mode.
2. Start the API server in the background.
3. Wait for the server to become available on port 8123.
4. Use `curl` to send a GET request to `/collatz/27`.
5. Use `curl` to send a POST request to `/determinant` with the following JSON payload:
   `{"matrix": [[2.0, -1.0, 0.0], [-1.0, 2.0, -1.0], [0.0, -1.0, 2.0]]}`
6. Parse the JSON responses (you may install and use `jq`).
7. Create a file at `/home/user/e2e_results.json` containing the extracted results strictly in this format:
   ```json
   {
     "collatz_27": <integer_length>,
     "determinant": <float_determinant>
   }
   ```
8. Gracefully terminate the background Rust server before the script exits.

Ensure `/home/user/run_e2e.sh` has executable permissions. You may install any system packages (like `jq` or `curl`) locally or use available tools. Do not assume any pre-existing code.