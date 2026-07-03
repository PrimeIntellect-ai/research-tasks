You are an AI assistant helping a machine learning engineer prepare training data. We need to analyze the stability of nearest neighbors in a feature space using bootstrap methods on the feature dimensions.

Here is your task:

1. **Environment Setup**:
   Create a Python virtual environment at `/home/user/venv`.
   Install `numpy` and `scikit-learn` in this environment.

2. **Data Analysis Script**:
   Write a script at `/home/user/analyze.py` that processes a dataset of feature vectors.
   The dataset is located at `/home/user/data/vectors.csv`. It contains 100 rows and 10 columns (comma-separated, no header).

3. **Algorithm Specifications**:
   In your script, perform the following:
   - Load the dataset into a numpy array (let's call it `X`).
   - Call `numpy.random.seed(42)` exactly **once** right after loading the data, before any loops.
   - For each row index `i` from 0 to 99 (in order):
     1. Compute the cosine similarity between row `i` and all other rows `j` (where `j != i`) using all 10 feature dimensions.
     2. Identify the original nearest neighbor `NN(i)` (the row index `j` with the highest cosine similarity). If there is a tie, pick the smallest index `j`.
     3. Perform 100 bootstrap iterations (loop `k` from 0 to 99). In each iteration:
        - Sample 10 column indices with replacement using `numpy.random.choice(10, size=10, replace=True)`.
        - Calculate the cosine similarities between row `i` and all other rows `j` (`j != i`) using **only** the sampled column indices.
        - Identify the bootstrap nearest neighbor `NN_boot(i)` using the same logic and tie-breaking as above.
        - Check if `NN_boot(i) == NN(i)`.
     4. Calculate the stability score for row `i` as the fraction of the 100 bootstrap iterations where `NN_boot(i) == NN(i)`.

4. **Output**:
   Save a JSON file to `/home/user/nn_stability.json` containing a dictionary mapping the row index (as a string, e.g., `"0"`, `"1"`) to its stability score (a float between 0.0 and 1.0).

Please execute the necessary commands to set up the environment, write the script, and run it to produce `/home/user/nn_stability.json`.