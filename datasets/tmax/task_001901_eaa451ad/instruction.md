You are an MLOps engineer managing an internal experiment tracking API written in Rust. This API enforces data schemas for probabilistic model parameters, performs Bayesian updates (calculating posterior distributions from priors and likelihoods), and aggregates tabular data for reproducibility testing.

A vendored version of the tracker source code has been placed at `/app/bayesian_tracker-1.0.0/`. However, the previous engineer left it in a broken state. It currently does not compile due to a deliberate error in its project files, and its run script is misconfigured.

Your tasks are:
1. Navigate to `/app/bayesian_tracker-1.0.0/` and identify the perturbation preventing compilation (hint: check `Cargo.toml` for syntax errors). Fix it.
2. The service requires an authentication token to be passed via an environment variable. Inspect the source code to determine the exact environment variable name expected, and run the service using the token `Baye$ian2023`.
3. The service must bind to exactly `127.0.0.1:9090`. You may need to provide this as an argument or environment variable, depending on how the code is structured.
4. Build and start the service in the background. Redirect its standard output and standard error to a log file at `/home/user/service.log`. 
5. Do not terminate the service; leave it running so our automated test suite can verify its endpoints.

The automated test will send HTTP requests to verify the schema enforcement, tabular aggregation, and Bayesian calculation logic. You do not need to send these requests yourself, only ensure the service is running, stable, and authenticated correctly.