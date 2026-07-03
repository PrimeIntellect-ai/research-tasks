You are an AI assistant helping a data science researcher organize a messy directory of experiments. 

The researcher has a directory at `/home/user/experiments/` containing multiple subdirectories (`exp_alpha`, `exp_beta`, `exp_gamma`). Each subdirectory contains:
1. `architecture.json`: Specifies the dimensions of a simple Multi-Layer Perceptron (MLP). It contains keys `input_dim`, `hidden_dim`, and `output_dim`.
2. `weights.npz`: A NumPy archive containing the weights and biases for the network. The arrays are named `W1`, `b1`, `W2`, `b2`.
3. `features.csv`: A headerless CSV file containing 50 rows of numerical data, where the number of columns matches `input_dim`.

Your task is to build a multi-language pipeline (using Bash and Python) to reconstruct these models, run inference, track the results, and organize the directories based on the output.

**Step 1: Inference Script (`/home/user/run_inference.py`)**
Write a Python script using `numpy` that takes a directory path as a command-line argument. The script must:
- Parse `architecture.json`.
- Load `weights.npz`.
- Read `features.csv`.
- Perform a forward pass: 
  - Hidden Layer: $Z_1 = X \cdot W_1 + b_1$
  - Activation: $A_1 = \max(0, Z_1)$ (ReLU)
  - Output Layer: $Z_2 = A_1 \cdot W_2 + b_2$
- Calculate the mean value of the final output $Z_2$ across all 50 rows.
- Print ONLY this mean float value to standard output.

**Step 2: Experiment Tracking & Organization Pipeline (`/home/user/organize.sh`)**
Write a Bash script that iterates over all subdirectories in `/home/user/experiments/`. For each experiment:
- Call `run_inference.py` to get the mean output score.
- Track this run by inserting a record into a SQLite database located at `/home/user/experiment_tracking.db`. The table should be named `results` with columns `experiment_name` (TEXT) and `mean_score` (REAL). Create the database and table if they do not exist.
- Organize the dataset:
  - If the `mean_score` is greater than `0.0`, move the entire experiment subdirectory into `/home/user/organized_data/positive/`.
  - Otherwise, move it into `/home/user/organized_data/negative/`.

Ensure you create `/home/user/organized_data/positive/` and `/home/user/organized_data/negative/` before moving files.

Run your `/home/user/organize.sh` script to complete the task.