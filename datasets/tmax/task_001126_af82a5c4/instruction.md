You are a data scientist tasked with building a data filtering pipeline for a fleet of mechanical sensors. Some sensors are malfunctioning and producing unstable readings that ruin our downstream predictive models. 

Your goal is to build a Rust-based command-line tool that classifies a given sensor dataset as either `CLEAN` or `EVIL` by checking if a simple linear regression model converges on the data.

**Audio Instructions:**
A senior engineer left a field recording containing the precise hyperparameters you must use for the convergence test. The audio file is located at `/app/field_notes.wav`. You will need to transcribe this file to find the required **learning rate** and **maximum iteration limit**.

**Dataset:**
The sensor data is provided as CSV files (with headers `x,y`). 
- Normal operational data is in `/app/data/clean/`.
- Anomalous, unstable data is in `/app/data/evil/`.

**Algorithm Requirements:**
You must implement standard Gradient Descent for a simple 1D linear regression: $y = mx + c$.
- Cost Function: Mean Squared Error $MSE = \frac{1}{2N} \sum_{i=1}^{N} (mx_i + c - y_i)^2$.
- Initial weights: $m = 0.0$, $c = 0.0$.
- Update rule: Compute gradients over the entire dataset (Batch Gradient Descent) and update weights simultaneously.
- Convergence condition: The model is considered to have converged if the absolute change in MSE between two consecutive epochs is strictly less than $10^{-5}$.
- The model fails to converge (is EVIL) if it hits the maximum iteration limit without converging, or if it encounters numerical instability (e.g., MSE becomes `NaN` or `Infinity`).

**Deliverable:**
1. Create a Rust project at `/home/user/filter_model`.
2. Write a CLI application that accepts a single file path as an argument.
3. Build the project in release mode. The binary should be at `/home/user/filter_model/target/release/filter_model`.
4. When executed as `/home/user/filter_model/target/release/filter_model <path-to-csv>`, the program MUST output exactly `CLEAN` (followed by a newline) if the gradient descent converges within the limits, and exactly `EVIL` (followed by a newline) if it diverges, becomes unstable, or fails to converge. No other stdout is permitted.

Ensure your application handles CSV parsing and strictly follows the hyperparameters dictated in the audio file.