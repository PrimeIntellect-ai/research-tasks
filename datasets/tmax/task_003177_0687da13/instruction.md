You are an observability engineer tasked with tuning a custom metrics pipeline and automating its staged deployment. 

We have a multi-service metrics stack located in `/app/`.
The stack consists of:
1. **Emitter Service:** Generates high-frequency log data on local port 8081.
2. **Rust Metrics Processor:** Listens on port 8082, fetches logs, computes a moving average of response times, and stores them. The source code is in `/app/rust_processor/`.
3. **Interactive Deployer:** A script `/app/deploy_manager.py` that handles rolling deployments of the Rust processor.

Recently, the dashboard has been timing out because the Rust metrics processor is too slow when handling large log batches. 

Your tasks are:
1. **Backup Strategy:** Before making any changes, back up the current compiled binary (`/app/rust_processor/target/release/metrics_processor`) and its data file (`/app/data/metrics.db`) to `/home/user/backup/`. The backup directory must be created if it does not exist.
2. **Code Optimization (Rust):** Inspect `/app/rust_processor/src/main.rs`. There is a severe performance bottleneck in the `compute_moving_average` function (currently using an O(N^2) vector insertion strategy like `vec.insert(0, item)`). Optimize this function so it processes data in O(N) time (e.g., using `push` or an iterator). Ensure the mathematical output remains exactly the same.
3. **Build:** Rebuild the Rust project in release mode.
4. **Automated Staged Deployment (Expect):** The deployer script `python3 /app/deploy_manager.py --binary /app/rust_processor/target/release/metrics_processor` requires interactive confirmation for staged rollouts. It will prompt:
   - `Deploy to stage 1 (10%)? [y/N]:`
   - `Deploy to stage 2 (50%)? [y/N]:`
   - `Deploy to stage 3 (100%)? [y/N]:`
   - `Commit rollout? [y/N]:`
   Write an Expect script at `/home/user/deploy.exp` that automates running the deploy manager and answers `y` to all these prompts. 
5. Run your expect script to deploy the new optimized binary.

Ensure the new processor is running and properly deployed. An automated benchmark will be run against port 8082 to verify that the processing throughput metric threshold is met.