You are an AI assistant helping a data analyst set up a local backend service for A/B testing analysis. 

We have a Rust-based HTTP microservice located at `/app/ab_service` that performs Bayesian inference and hypothesis testing on CSV data. This service enforces a strict data schema on the input CSV, configures a numerical library for calculating posterior distributions, and exposes the results over HTTP.

However, the service currently does not compile or run due to a configuration issue in its vendored dependencies.

Your task is to:
1. Investigate the vendored Rust package at `/app/ab_service`. There is an intentional configuration error in the `build.rs` file related to the numerical library configuration environment variable `MATH_CONFIG`. It is currently set to an invalid string, causing the build to fail. Fix this by changing it to the expected value: `bayes_v1`.
2. Compile the service using `cargo build --release` (you must run this inside `/app/ab_service`).
3. The service requires an input CSV file at `/home/user/data.csv`. Create this file with the following exact content (enforcing the expected schema: `variant_name,trials,successes`):
```csv
variant_name,trials,successes
control,1000,150
treatment,1000,180
```
4. Run the compiled binary (`/app/ab_service/target/release/ab_service`). It will automatically bind to `127.0.0.1:8888` and parse the CSV file.
5. Leave the service running in the background.

The data analyst's automated tools will query this service via HTTP to retrieve the calculated Bayesian confidence intervals and statistical summaries. The service is protected by an authorization token.

Ensure the service is fully running and listening on the specified port. Use shell commands (`sed`, `echo`, `cargo`, etc.) to accomplish this.