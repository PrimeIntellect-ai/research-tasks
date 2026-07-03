You are a build engineer managing an artifact generation pipeline. We have a mathematical character encoder tool built with Rust and exposed via a Python web server. The encoder takes a string and a numeric shift parameter, then computes a new unicode value for each character using the mathematical transformation `new_val = char_val + shift^2`.

Currently, the pipeline is broken:

1. The Rust code located in `/home/user/rust_encoder/` fails to compile due to a borrow checker error in `src/main.rs`. Identify and fix the borrow checker error. Once fixed, build the project using `cargo build`.
2. The Python web server at `/home/user/server.py` has a bug in its URL parameter parsing. It is designed to handle requests to the `/encode` route and extract the `msg` and `shift` query parameters, but the extraction logic for the shift parameter is flawed. Fix the parameter parsing logic in the Python script.
3. Start the Python server so it listens on `127.0.0.1:8080` in the background.
4. Using `curl`, make a GET request to the server with the parameters `msg=Agent` and `shift=3`. Save the raw response body directly to a file located at `/home/user/artifact.txt`.

Ensure the response written to ``/home/user/artifact.txt`` is exactly the output produced by the server, with no additional formatting.