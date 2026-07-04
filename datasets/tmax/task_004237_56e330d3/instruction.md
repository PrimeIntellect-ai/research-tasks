You are a Data Engineer tasked with building a lightweight ETL and experiment-tracking pipeline for a text classification problem. 

You have been provided with a dataset at `/home/user/dataset.tsv` (which contains two tab-separated columns: `label` and `text`). The `label` is either `0` or `1`.

Your objective is to build a multi-stage pipeline using Bash and Python that tokenizes the text, extracts features, trains a baseline classification model, and tracks the experiment results.

Write the following scripts:

1. **`prep.sh` (Data Preparation & Tokenization)**
   - Must be an executable bash script located at `/home/user/prep.sh`.
   - Accepts a single integer argument `N` (e.g., `./prep.sh 5`).
   - Reads `/home/user/dataset.tsv`.
   - Cleans the `text` column: converts all characters to lowercase and replaces all non-alphanumeric characters with a single space.
   - Tokenizes the text by space.
   - Determines the top `N` most frequent words across the entire dataset (break ties alphabetically if necessary).
   - Generates a CSV file at `/home/user/features.csv`.
   - The first row of `features.csv` must be a header containing the `N` words followed by `label` (e.g., `the,error,user,label`).
   - Subsequent rows must correspond to the lines in `dataset.tsv`. Each column for a word should contain `1` if the word is present in that cleaned text, and `0` otherwise. The last column is the integer `label`.

2. **`train.py` (Classification)**
   - Must be a Python script located at `/home/user/train.py`.
   - Reads `/home/user/features.csv`.
   - Uses `sklearn.linear_model.LogisticRegression` (with `random_state=42`, and all other default parameters).
   - Fits the model on the entire dataset (features = word columns, target = label).
   - Calculates the accuracy of the model on the same dataset.
   - Prints *only* the accuracy to standard output as a float (e.g., `0.75`).

3. **`track.sh` (Experiment Tracking)**
   - Must be an executable bash script located at `/home/user/track.sh`.
   - Takes no arguments.
   - For the values of `N` in `3`, `5`, and `10`:
     - Runs `./prep.sh N`.
     - Runs `python3 train.py` and captures the output.
     - Appends a single line of JSON to `/home/user/experiments.jsonl` in the exact format: `{"n_words": N, "accuracy": <accuracy_value>}`.

Make sure you install any necessary Python packages (like `pandas` and `scikit-learn`) using `pip` before running your scripts.