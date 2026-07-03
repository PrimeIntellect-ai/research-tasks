You are a data engineer building an ETL and modeling pipeline for a text classification task.

You have been provided with a dataset at `/home/user/data.csv` and a modeling script at `/home/user/pipeline.py`. 
Currently, the pipeline has a critical flaw: a data leakage issue where the TF-IDF embedding vectorizer is fitted on the entire dataset *before* the train/test split. 

Your tasks are:
1. **Fix the Data Leak:** Modify `/home/user/pipeline.py` so that the dataset is split into training and testing sets *first* (using `test_size=0.3` and `random_state=42`). Then, fit the `TfidfVectorizer` only on the training text, and transform both the train and test texts. Leave all other random states and hyperparameter configurations as they are.
2. **Ensure Reproducibility via Bash:** Write a Bash wrapper script at `/home/user/evaluate.sh` that runs the Python script. To guarantee pipeline reproducibility across different numerical libraries and hashing algorithms, this Bash script must export `PYTHONHASHSEED=42` and `OMP_NUM_THREADS=1` before executing `/home/user/pipeline.py`.
3. **Capture Output:** The Bash script `/home/user/evaluate.sh` must redirect the output of the Python script (which prints the accuracy as a float) to `/home/user/accuracy.txt`.

Ensure your Bash script is executable (`chmod +x`). 
Do not change the `train_test_split` parameters other than what you pass to it. Keep the logistic regression's `random_state=42`.