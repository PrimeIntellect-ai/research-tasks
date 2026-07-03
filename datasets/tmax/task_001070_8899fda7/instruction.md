You are an AI assistant helping a data scientist fit models to a massive set of sensor observations. We need to identify which two sensors have the most similar data distributions to eliminate redundant features in our models. 

Your objective is to build a high-performance Rust application that reshapes the observational data, computes the Jensen-Shannon Divergence (JSD) between all pairs of sensors in parallel, and then orchestrate this workflow using a Jupyter Notebook.

### 1. Data Processing and Rust Application
The raw data is located at `/home/user/data/observations.csv`. It has a header and three columns: `timestamp` (string), `sensor_id` (string), and `value` (float between 0.0 and 1.0).

Create a Rust project at `/home/user/rust_dist/`. The application must:
1. Parse the CSV file and group the values by `sensor_id`.
2. For each sensor, compute a 10-bin histogram of its values. The bins are `[0.0, 0.1)`, `[0.1, 0.2)`, ..., `[0.9, 1.0]`. If a value is exactly `1.0`, it belongs in the final bin.
3. Apply Laplace smoothing to avoid zero probabilities: Add exactly `1e-9` to the count of *every* bin. Then, normalize the bin counts so they sum to 1.0, resulting in a probability distribution for each sensor.
4. Calculate the Jensen-Shannon Divergence (JSD) between all unique pairs of sensors. 
   - $M = \frac{1}{2}(P + Q)$
   - $KLD(P || M) = \sum P(i) \ln\left(\frac{P(i)}{M(i)}\right)$
   - $JSD(P, Q) = \frac{1}{2} KLD(P || M) + \frac{1}{2} KLD(Q || M)$ (use the natural logarithm)
5. **Parallelism Requirement**: You must use the Rust `rayon` crate to compute the pairwise JSDs in parallel.
6. The Rust program must output the results as a JSON array to `/home/user/output/distances.json`. Each object in the array should look like:
   `{"sensor_a": "S1", "sensor_b": "S2", "jsd": 0.00123}`
   Only include unique pairs, and always ensure that `sensor_a` is lexicographically strictly less than `sensor_b`.

### 2. Notebook-Based Workflow Orchestration
We need this workflow to be reproducible in a notebook environment.
Create a Jupyter Notebook at `/home/user/workflow.ipynb` (using a Python 3 kernel) that performs the following orchestration steps when run cell-by-cell:
1. Compiles the Rust project in release mode (`cargo build --release`).
2. Executes the compiled Rust binary to generate the `distances.json` file.
3. Reads `distances.json` using Python.
4. Finds the pair of sensors with the smallest JSD (the most similar pair).
5. Writes the names of these two sensors, comma-separated and lexicographically sorted, to `/home/user/output/best_pair.txt` (e.g., `S3,S7`).

### Setup and Deliverables
- The data is already at `/home/user/data/observations.csv`.
- Create the `/home/user/output/` directory yourself.
- Execute your notebook (e.g., using `jupyter nbconvert --to notebook --execute /home/user/workflow.ipynb` or `papermill`) to ensure all outputs are generated.
- The task is complete when `/home/user/output/best_pair.txt` and `/home/user/output/distances.json` exist and contain the correct values.