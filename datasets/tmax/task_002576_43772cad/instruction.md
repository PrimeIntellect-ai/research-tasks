I need you to fix a broken polyglot mathematical computation system. 

We have a Rust CLI tool located in `/home/user/math_engine` that is supposed to perform high-precision mathematical operations, but it currently fails to compile because `src/constants.rs` is incomplete. 

I don't remember the exact missing values, but I saved a screenshot of the original specifications in `/app/system_spec.png`. You will need to extract the text from this image (you can use `tesseract`). The image contains two critical pieces of information:
1. `MATH_MAGIC_CONSTANT`: A high-precision float that you must add to `src/constants.rs` (as a `pub const` `f64`) so the Rust project compiles successfully.
2. `API_TOKEN`: A secret string used for authentication.

Here are your objectives:
1. **Fix the Rust Project**: Read the image, extract the constant, fix the code in `/home/user/math_engine/src/constants.rs`, and compile the Rust project in release mode. The resulting binary will take a single integer argument `N` and print the result of `N * MATH_MAGIC_CONSTANT` to stdout.
2. **Create a Go API Server**: Write a Go HTTP server in `/home/user/go_server/main.go` and run it in the background. 
   - It must listen on `127.0.0.1:8080`.
   - It must expose a `POST /compute` endpoint that accepts JSON in the format: `{"value": <int>}`.
   - It must secure the endpoint by checking for the `Authorization: Bearer <API_TOKEN>` header (using the token extracted from the image). Return a 401 Unauthorized HTTP status if missing or invalid.
   - For valid requests, the Go server should use a goroutine to securely execute the compiled Rust binary (`/home/user/math_engine/target/release/math_engine`), pass the integer value, read the output, and respond with JSON: `{"computed": <float>}`.
   - The Go server must be able to handle concurrent requests efficiently.

Initialize the Go module, write the server, start it in the background, and ensure the port `8080` is open and listening before you finish the task.