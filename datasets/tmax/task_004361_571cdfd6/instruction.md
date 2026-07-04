You are a support engineer tasked with recovering a critical diagnostic aggregation system for a financial client. The system consists of a Rust-based `compute-engine` that calculates real-time statistical metrics, and an API gateway (`nginx`) that exposes this service. 

Currently, the system is completely offline and plagued by several bugs introduced in a recent messy commit. Your goal is to debug, fix, and integrate the components so they work seamlessly end-to-end.

Workspace:
- `/app/compute-engine/`: The Rust backend service.
- `/app/gateway/nginx.conf`: The Nginx configuration file for the API gateway.
- `/app/start.sh`: A shell script that will be used to launch both Nginx and the Rust backend.

Issues to resolve:
1. **Dependency Conflict**: The `compute-engine` fails to compile. There is a version conflict in `/app/compute-engine/Cargo.toml` between `tokio` and `axum`. You must resolve this so `cargo build` succeeds without errors.
2. **Format Parsing Edge-Cases**: The Rust service parses comma-separated floats from an API request. However, it currently crashes (panics) when it encounters "NaN", "infinity", or unparseable text (like "N/A"). You must modify the code to safely ignore/filter out any string that cannot be parsed into a valid finite float, processing only the valid numbers.
3. **Floating-point & Numerical Instability**: The variance calculation formula in `/app/compute-engine/src/main.rs` is naively implemented using `f32` and a single-pass sum of squares formula: `(sum_sq / n) - (mean * mean)`. This suffers from catastrophic cancellation on datasets with large baselines and small variances. You must refactor the calculation to use `f64` throughout and implement a numerically stable algorithm (e.g., Welford's online algorithm or a reliable two-pass method) to ensure exact precision.
4. **Service Integration**: The `compute-engine` binds to `127.0.0.1:9000`. The API gateway needs to listen on `127.0.0.1:8080`. You must update `/app/gateway/nginx.conf` so that HTTP GET requests to `http://127.0.0.1:8080/compute` correctly reverse-proxy to the Rust backend.

Output specifications:
- The endpoint `/compute?input=...` must return a JSON object with strictly these two keys: `{"mean": <float>, "variance": <float>}`.
- If less than 2 valid data points are provided, `variance` should be `0.0`.
- Once you have fixed the code and configurations, ensure you can run `bash /app/start.sh` successfully to bring both services up. Keep them running so the automated test suite can verify the endpoint.