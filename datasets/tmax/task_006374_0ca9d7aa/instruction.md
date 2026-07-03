You are helping a researcher organize their dataset and fix an automated experiment tracking pipeline. 

The researcher has a script located at `/home/user/inference.py` and a dataset at `/home/user/data.csv`. The script performs a basic model reconstruction, runs inference, tracks the experiment metric by writing to a JSON file, and plots the results. 

However, there are two problems:
1. The researcher needs to evaluate the model on a bootstrap sample of the dataset, but they haven't created the sample.
2. The Python script runs, but the output plot (`output.png`) is always completely blank (white) due to a common misconfiguration with how the plot is saved/displayed.

Your tasks:
1. Create a bootstrap sample of `/home/user/data.csv`. A bootstrap sample is a random sample taken *with replacement* that has the exact same number of rows as the original dataset. Save this sample to `/home/user/bootstrap.csv`.
2. Fix the bug in `/home/user/inference.py` so that it successfully saves the plot with the actual data points and regression line, rather than a blank image. (Hint: look at the order of matplotlib commands).
3. Run the fixed `/home/user/inference.py` using your newly created `/home/user/bootstrap.csv` as the input argument.

To complete the task, the following final state must be met:
- `/home/user/bootstrap.csv` exists, contains the exact same number of rows as `data.csv`, and its rows are sampled with replacement from `data.csv`.
- `/home/user/output.png` exists and is a valid, non-blank image (file size should be significantly larger than a blank 1x1 or empty plot, typically > 5KB).
- `/home/user/metrics.json` exists and contains the tracked experiment metric from running the script on the bootstrap sample.