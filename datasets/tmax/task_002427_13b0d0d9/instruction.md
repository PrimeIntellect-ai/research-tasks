You are assisting a researcher who is organizing and preparing a dataset of sensor measurements for downstream statistical modeling. The dataset contains a target variable and multiple continuous features, but it is extremely messy. 

The raw dataset is located at:
`/home/user/data/raw.csv`

The researcher has an old proprietary evaluation tool that scores the quality of a dataset based on its correlation with the target and its internal covariance structure. The tool has been provided as a stripped Linux binary:
`/app/evaluator`

Your task is to write a Python script that processes `raw.csv` and outputs a cleaned dataset to:
`/home/user/data/clean.csv`

Requirements:
1. Load `/home/user/data/raw.csv`.
2. Handle missing values appropriately.
3. Identify and handle extreme outliers.
4. Perform feature selection and engineering to maximize the score given by `/app/evaluator`. The evaluator takes one argument: the path to the CSV file.
   Example: `/app/evaluator /home/user/data/clean.csv`
5. The output `clean.csv` must contain the `target` column and whichever features you choose to keep or create.

Your goal is to prepare `clean.csv` such that `/app/evaluator /home/user/data/clean.csv` outputs a score of **0.35 or higher**.