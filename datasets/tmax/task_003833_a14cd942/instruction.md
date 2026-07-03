You are a build engineer tasked with fixing and optimizing an internal artifact management system. We process thousands of artifact metadata records, and we recently started migrating our hot-path data deserialization to a Rust-based Python extension using PyO3 and Maturin to meet strict performance SLAs.

However, the current development environment is broken across several levels:
1. **Service Configuration**: The local metadata backend consists of a Flask application and a Redis cache. The Flask application is located at `/app/backend/app.py`. It runs on port 8080, but it currently fails to start because it cannot connect to Redis. You need to start a local Redis server (port 6379) and run the Flask app, ensuring it is properly configured to communicate with Redis using the `REDIS_URL` environment variable.
2. **Python Package Build**: The Python package at `/home/user/fast_artifact` has a broken `pyproject.toml`. It is missing the necessary build-backend configuration to compile the Rust extension via Maturin.
3. **Rust Compilation Errors**: The Rust extension code in `/home/user/fast_artifact/src/lib.rs` fails to compile due to a borrow checker error involving URL string parsing and parameter routing, as well as lifetime issues during JSON deserialization.
4. **Integration & Benchmarking**: Once the extension is compiled and installed in your environment, run the benchmark script at `/home/user/benchmark.py`. This script will use your compiled extension to fetch and deserialize 5,000 artifacts from `http://localhost:8080/api/artifact/<id>`. 

Your goal is to successfully fix the services, resolve the Rust errors, build the extension, and run the benchmark. The benchmark script automatically writes the processing time to `/home/user/metrics.json` in the format `{"total_time_seconds": 1.23}`. 

To complete this task, the total execution time recorded in `/home/user/metrics.json` must be strictly less than 1.5 seconds.