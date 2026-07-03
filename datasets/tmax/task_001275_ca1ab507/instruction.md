You are acting as an MLOps engineer tasked with creating a reproducible artifact tracking pipeline. We have a set of raw experiment results from recent model training runs, but they are scattered across directories and lack a unified summary. 

Your objective is to set up an isolated Python environment, install necessary dependencies, and write a reproducible Python script that parses these artifacts to generate a standardized summary report.

Here are your specific instructions:

1. **Environment Setup**: 
   Create a Python virtual environment at `/home/user/mlops_env`. 
   Inside this environment, install `pandas`. 

2. **Pipeline Construction**:
   Write a Python script named `/home/user/summarize_artifacts.py`. When run using the virtual environment's Python, it must process the experiment artifacts located in the directory `/home/user/experiments`.

   The `/home/user/experiments` directory contains subdirectories for each run (e.g., `run_alpha`, `run_beta`, etc.). Inside each run directory, you will find:
   - `config.json`: Contains a JSON object with hyperparameter settings.
   - `metrics.csv`: Contains training metrics per epoch. The columns are `epoch`, `loss`, and `accuracy`.
   - `model.pt`: A binary file representing the saved model weights.

   Your script must iterate through all run directories and extract:
   - `run_id`: The name of the run directory (e.g., `run_alpha`).
   - `learning_rate`: Extracted from the `learning_rate` key in `config.json`.
   - `final_accuracy`: The `accuracy` value from the row with the highest `epoch` number in `metrics.csv`.
   - `model_size_bytes`: The file size of `model.pt` in bytes.

3. **Output Generation**:
   The script must output a single CSV file at `/home/user/experiment_summary.csv`.
   The CSV must contain exactly the following columns in order: `run_id`, `learning_rate`, `final_accuracy`, `model_size_bytes`.
   The rows must be sorted by `final_accuracy` in descending order. If there is a tie, sort by `run_id` alphabetically.

Ensure your code is robust and your pipeline runs end-to-end to produce the final CSV. Run your script to generate `/home/user/experiment_summary.csv` before concluding the task.