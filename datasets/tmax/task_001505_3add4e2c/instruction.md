You are a performance engineer debugging a newly deployed telemetry analysis pipeline. 

We have a multi-service system located in `/app/telemetry_system` that monitors memory usage across our fleet. The system consists of:
1. **Redis** (running on port 6379) - Acts as the message broker for telemetry data.
2. **Telemetry Generator** (running as a local process) - Pushes simulated memory usage data (timestamps and bytes) to the Redis list `telemetry_stream`.
3. **JupyterLab** (running on port 8888) - Used for orchestrating workflows and prototyping data processing algorithms. 
4. **Rust Analyzer Service** (source in `/app/telemetry_system/analyzer`) - A Rust web service (runs on port 8080) that reads data from Redis and performs a polynomial curve fit (degree 2) to predict future memory usage and detect leaks.

**The Problem:**
The current implementation of the curve fitting algorithm in `/app/telemetry_system/analyzer/src/regression.rs` uses a naive Normal Equation ($X^T X \beta = X^T Y$) with a direct matrix inversion. Because the input features are raw Unix timestamps (which are very large numbers), the $X^T X$ matrix is ill-conditioned. This causes severe numerical instability: the resulting coefficients are wildly inaccurate or evaluate to NaN, making our performance predictions useless.

**Your Task:**
1. Start the background services by running `/app/telemetry_system/start_services.sh`.
2. Prototyping: You can use the Jupyter server to prototype a numerically stable regression approach (e.g., using standard scaling / Z-score normalization of the timestamp features before fitting, or using a more stable decomposition like QR).
3. Fix the Rust implementation in `/app/telemetry_system/analyzer/src/regression.rs`. You must implement standard scaling (centering by mean and scaling by standard deviation) for the independent variables (X) prior to fitting the polynomial, and ensure the prediction function scales inputs accordingly. 
4. Compile and start the Rust analyzer service (`cargo run --release` on port 8080).
5. Run the evaluation script `/app/telemetry_system/evaluate.py`. This script will inject a hidden set of performance data into Redis, query your Rust API for predictions, and calculate the Mean Squared Error (MSE) of your model's predictions.

**Acceptance Criteria:**
To succeed, the evaluator `/app/telemetry_system/evaluate.py` must output a final Mean Squared Error (MSE) strictly less than `0.05`. 
Do not modify the evaluation script or the telemetry generator.