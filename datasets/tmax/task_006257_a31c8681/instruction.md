You are a data analyst taking over a project. Your colleague wrote a Python script at `/home/user/pipeline.py` to preprocess a dataset located at `/home/user/dataset.csv`. 

However, the script has a critical **data leakage** bug. It applies missing value imputation (using the mean) and standard scaling to the *entire* dataset before splitting it into training and test sets. 

Your tasks are:
1. Identify and fix the data leakage in `/home/user/pipeline.py`. Modify the script so that the `SimpleImputer` and `StandardScaler` are **fitted only on the training data**, and then used to transform both the training and test sets. Maintain the same 80/20 train-test split and `random_state=42`.
2. Ensure you have the necessary dependencies installed (e.g., `pandas`, `scikit-learn`, `scipy`).
3. After fixing the pipeline and transforming the data correctly, calculate the **95% confidence interval** for the mean of `Feature_0` in the **transformed test set**. Use a Student's t-distribution for your confidence interval calculation (using `scipy.stats.t.interval`). 
4. Write the lower and upper bounds of this confidence interval to a file named `/home/user/ci_output.txt`. The file should contain exactly one line with the lower and upper bounds separated by a comma, rounded to 4 decimal places (e.g., `-0.1234,0.5678`).

The dataset `/home/user/dataset.csv` and the script `/home/user/pipeline.py` already exist. Fix the script in place and generate the CI output file.