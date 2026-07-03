You are a data engineer tasked with fixing and deploying a local ETL pipeline. 

We have a Python script located at `/home/user/etl.py` that processes a tabular dataset `/home/user/data.csv`. The script performs dimensionality reduction (PCA) and splits the data into train and test sets, then computes a simple aggregation (the mean of the first principal component for the test set) and writes it to `/home/user/etl_output.txt`.

However, the current pipeline has a critical data leakage bug. The dimensionality reduction step is being fitted on the entire dataset *before* the train-test split, causing information from the test set to leak into the training transformations.

Your tasks are:
1. **Environment Setup:** Create a Python virtual environment at `/home/user/venv` and install `pandas`, `scikit-learn`, and `numpy`.
2. **Fix the Python Pipeline:** Edit `/home/user/etl.py` to fix the data leakage. The `PCA` object should strictly be fitted only on the training features (`X_train`), and then used to transform both `X_train` and `X_test`. Keep `test_size=0.2` and `random_state=42` in the split, and `random_state=42` in PCA.
3. **Configure Numerical Libraries via Bash:** We need to ensure deterministic and single-threaded execution for our numerical backends. Create an executable Bash script at `/home/user/run_etl.sh`. This script must:
    - Activate the virtual environment.
    - Export the environment variables `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1`.
    - Execute the fixed Python script (`python3 /home/user/etl.py`).
4. **Run the Pipeline:** Execute your `/home/user/run_etl.sh` script to generate the corrected `/home/user/etl_output.txt`.

Ensure your Bash script is executable (`chmod +x`) and successfully outputs the correct single float value to the text file.