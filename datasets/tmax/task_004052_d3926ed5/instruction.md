You are an integration developer testing a high-throughput API for a distributed logging system. Our application uses a multi-service architecture located in `/app/`:
1. **API Service** (`/app/api.py`): A FastAPI application running on port 8000 that receives large batches of numerical data.
2. **Message Broker**: A Redis instance running on port 6379.
3. **Worker Service** (`/app/worker.py`): A Python worker that pulls data from Redis, computes a complex error-correcting checksum (a custom Reed-Solomon variant), and logs the result.

Currently, the worker uses a naive Python implementation of the checksum (`/app/utils/naive_checksum.py`), which is severely bottlenecking the system. 

We have started writing a high-performance Rust implementation in `/app/rust_ecc/`, intended to be exposed to Python via `maturin`. However, the Rust code currently has memory management (borrow checker) errors and the `Cargo.toml` is missing some dependency configurations for PyO3.

Your objectives are:
1. **Fix the Rust Implementation**: Navigate to `/app/rust_ecc/` and fix the borrow checker errors in `src/lib.rs`. Ensure the package dependencies in `Cargo.toml` are correctly configured for PyO3 to build a Python module named `rust_ecc`.
2. **Build and Install**: Build the Rust extension using `maturin` and install it into the system Python environment.
3. **Reconfigure the System**: Modify `/app/worker.py` to import and use `rust_ecc.compute_checksum(data)` instead of the naive Python implementation.
4. **Bring up the Services**: Ensure Redis, the FastAPI app, and the worker process are all running and correctly communicating.
5. **Benchmark**: We have provided a benchmarking script at `/app/benchmark.py`. When you run this script, it blasts the API with requests and outputs the processed `requests_per_second`. 

To succeed, you must optimize the system such that the benchmark script reports a throughput of at least 800 requests per second. Run the benchmark, verify the performance, and leave the optimized services running.