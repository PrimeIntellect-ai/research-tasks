You are an open-source maintainer reviewing a broken Pull Request for a mathematical visualization project. The project runs a WebSocket server in Python that streams the results of a computationally heavy dynamical system (a 2D iterative map) to clients. 

A contributor recently submitted a PR to rewrite the core mathematical engine in Rust (using PyO3) to improve performance. However, the PR is broken and has several issues:
1. The Rust code fails to compile due to ownership and borrow checker errors.
2. The build system configuration (`pyproject.toml` / `Cargo.toml`) is misconfigured, preventing the Python module from linking correctly.
3. The WebSocket server (`server.py`) has a bug in how it serializes the mathematical data received from the Rust engine before sending it over the connection.

Additionally, a user submitted a screenshot of the specific mathematical parameters they used when they experienced a crash on the old system. This screenshot is located at `/app/sys_config.png`.

Your objectives are:
1. Use OCR (e.g., `tesseract`, which is preinstalled) to extract the parameters from `/app/sys_config.png`. The image contains three key-value pairs: `ALPHA`, `BETA`, and `ITERATIONS`.
2. Fix the Rust source code in `/home/user/math_ws_project/rust_engine/src/lib.rs` so it compiles successfully.
3. Fix the build configuration so the Rust extension can be built and installed (you can use `maturin develop` or `pip install -e .` depending on the setup).
4. Fix the serialization logic in `/home/user/math_ws_project/server.py`.
5. Write a script `run_benchmark.py` that imports both the old pure-Python implementation (provided in `pure_python.py`) and the new Rust implementation. It must compute the trajectories using the parameters extracted from the image.
6. Calculate the Mean Squared Error (MSE) between the final coordinate arrays of both implementations to ensure correctness.
7. Calculate the speedup factor: `(time_pure_python / time_rust)`.
8. Output the final metrics to a JSON file at `/home/user/benchmark_results.json` with the exact keys: `"mse"` (float) and `"speedup"` (float).

You must achieve an exact mathematical match (MSE < 1e-5) and a speedup of at least 3.0x.