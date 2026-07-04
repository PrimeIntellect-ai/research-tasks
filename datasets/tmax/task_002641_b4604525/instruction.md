I need you to fix a broken vendored Python package that wraps a Rust-based URL parser, and then write a Python script that perfectly emulates our legacy C-based parser's output. 

We have a vendored package located at `/app/vendored/rust_url_parser`. It is a multi-file Rust project built as a Python extension using PyO3, but it currently fails to compile. The build system (using `maturin`) has a deliberate configuration error in its `pyproject.toml` and a memory-safety/undefined behavior bug in the Rust string handling logic that prevents the routing module from safely decoding URL parameters.

Your tasks are:
1. Identify and fix the compilation issues in `/app/vendored/rust_url_parser` so that the Python extension successfully builds and installs. You may need to patch the Rust code to fix the memory parsing logic.
2. Build and install the package into the local Python environment.
3. Write a Python script at `/home/user/run_parser.py` that imports this newly compiled module. 
4. The script must read standard input (which will provide a raw URL on each line) and output a JSON object per line. The JSON must contain the extracted route, protocol, and a hex-encoded transformation of the URL parameters. 

Your Python script's output must be bit-for-bit identical to our legacy C binary, which acts as the oracle. The automated verifier will fuzz your script against the oracle using thousands of randomized malformed and well-formed URLs. Make sure you handle character encodings properly, as the fuzzing will include complex UTF-8 sequences.