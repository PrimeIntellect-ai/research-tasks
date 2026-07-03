You are an MLOps engineer responsible for building a lightweight, Bash-based experiment tracking system for a text classification project. We want to avoid heavy dependencies like MLflow and instead use a custom Bash pipeline that handles data preparation, model training, and artifact tracking.

Your objective is to create a fully automated Bash script named `/home/user/run_pipeline.sh` that orchestrates a machine learning experiment. 

Here are the requirements:

1. **Setup**:
   - Install `scikit-learn` and `pandas` using pip.
   - You are provided a raw dataset at `/home/user/data/dataset.csv` with two columns: `text` and `label` (0 or 1).

2. **The Pipeline Script (`/home/user/run_pipeline.sh`)**:
   - The script must accept two named arguments: `--max_features` (integer) and `--c_value` (float).
   - **Tokenization/Preparation (Bash)**: Before passing data to Python, the Bash script must create a processed version of the dataset at `/home/user/data/processed.csv`. It should convert all text in `dataset.csv` to lowercase and remove all punctuation (except the commas separating the CSV columns). 
   - **Training**: The script should invoke a Python script (which you must also write, e.g., `/home/user/train.py`) that:
     - Reads `/home/user/data/processed.csv`.
     - Uses `TfidfVectorizer` with `max_features` set to the provided argument.
     - Trains a `LogisticRegression` model with `C` set to the provided argument and `random_state=42`.
     - Prints the training accuracy to standard output (just the float value, e.g., `0.852`).
     - Saves the trained model to a file named `model.pkl`.
   - **Experiment Tracking (Bash)**: 
     - Generate a unique Experiment ID using the current Unix timestamp (e.g., `1690000000`).
     - Create a directory for the experiment artifacts at `/home/user/artifacts/exp_<TIMESTAMP>/`.
     - Move the `model.pkl` and `processed.csv` into this artifact directory.
     - Append a record to `/home/user/experiments.csv` in the exact format: `timestamp,max_features,c_value,accuracy`. Create the file with a header row `id,max_features,C,accuracy` if it doesn't exist.

Write the scripts, ensure `/home/user/run_pipeline.sh` is executable, and test it by running:
`/home/user/run_pipeline.sh --max_features 100 --c_value 1.0`

Leave the system in a state where I can programmatically read `/home/user/experiments.csv` and inspect the artifacts directory to verify your work.