You are an ML Engineer tasked with preparing a training dataset entirely using shell utilities. Your company restricts the use of Python, R, or any external data science libraries on this specific preprocessing node. You must build a robust, reproducible bash pipeline to clean the data and perform feature selection before passing it to our proprietary model evaluator.

**Context:**
You are given a raw dataset at `/home/user/raw_data.csv`. It has 11 columns. The first 10 columns (`f1` to `f10`) are continuous numerical features. The 11th column (`target`) is a binary label (`0` or `1`).
There is a stripped, proprietary binary provided at `/app/model_evaluator` which takes a prepared CSV file, trains an internal model, and outputs an accuracy metric.

**Your Objective:**
Write a bash script at `/home/user/prepare_data.sh` that performs the following steps strictly using bash built-ins, `awk`, `sed`, and `coreutils`:

1.  **Data Cleaning:** Remove any row from `raw_data.csv` that contains the character `?` (representing missing data). Be careful not to accidentally convert missing values to `0` or `NaN` strings.
2.  **Correlation Analysis:** Compute the Pearson correlation coefficient between each of the 10 features and the `target` column based on the cleaned data.
3.  **Feature Selection:** Select the top 5 features that have the highest *absolute* Pearson correlation with the target.
4.  **Dataset Generation:** Output a final dataset named `/home/user/train_clean.csv` containing only the selected 5 features and the target column (which must remain the last column). The header must be preserved, containing only the names of the selected features and the target.

**Evaluation:**
Once your dataset is ready, run it through the evaluator:
`/app/model_evaluator /home/user/train_clean.csv`

This tool will output a string like: `EVALUATION COMPLETED. ACCURACY=0.88`

You must iterate on your `prepare_data.sh` script until the generated dataset achieves an accuracy of at least **0.85**. 

**Constraints:**
- You must write the solution entirely in Bash (using `awk`, `grep`, `sort`, `cut`, etc. is allowed and expected).
- Do not use Python, Perl, Node.js, or any other scripting languages.
- Your script `/home/user/prepare_data.sh` must be completely reproducible and run without human intervention.