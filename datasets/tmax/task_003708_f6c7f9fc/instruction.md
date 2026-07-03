You are a machine learning engineer tasked with preparing training data and extracting the Maximum A Posteriori (MAP) weights for a Bayesian Linear Regression model. You must implement this pipeline in Rust.

Your goal is to create a Rust project that reads a dataset, performs feature engineering, calculates the MAP estimates using matrix algebra, and logs the experiment metadata and results.

Here are the specific requirements:

1. Setup:
   - Create a new Rust project named `bayesian_data_prep` in `/home/user/bayesian_data_prep`.
   - Add any necessary dependencies (e.g., `csv`, `nalgebra`, `serde_json`) to your `Cargo.toml`.

2. Feature Engineering & Selection:
   - Read the dataset located at `/home/user/data/raw_measurements.csv`. 
   - The CSV contains the following headers: `temp`, `pressure`, `humidity`, `vibration`, `failure_score`.
   - Construct a design matrix $X$ where each row is a sample.
   - For the features, include a bias term (always `1.0`) as the first column, followed by `temp`, `pressure`, and `humidity` (strictly in that order). Drop the `vibration` column.
   - Construct the target vector $Y$ using the `failure_score` column.

3. Bayesian Inference & Linear Algebra:
   - Assuming a Gaussian likelihood and an isotropic Gaussian prior on the weights, compute the MAP estimate of the weights $W$.
   - The formula for the MAP estimate (equivalent to Ridge Regression) is:
     $W = (X^T X + \lambda I)^{-1} X^T Y$
   - Use a prior precision (regularization parameter) of $\lambda = 2.0$.
   - Note: $I$ is the identity matrix of the same dimension as $X^T X$.

4. Experiment Tracking:
   - Create the directory `/home/user/experiment` if it doesn't exist.
   - Save the computed weights $W$ as a flat JSON array of 4 floats (bias, temp_weight, pressure_weight, humidity_weight) to `/home/user/experiment/weights.json`.
   - Save metadata about the dataset as a JSON object to `/home/user/experiment/metadata.json` with the following exact keys:
     - `"n_samples"`: the number of rows processed.
     - `"n_features"`: the number of columns in $X$ (which should be 4).

Execute the commands to build and run your Rust program so that the final JSON files are successfully created. Do not round the floating-point values in the JSON output.