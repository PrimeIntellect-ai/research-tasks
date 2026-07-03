You are an AI assistant helping a data science researcher organize their raw data files and build a simple reproducible evaluation pipeline. 

The researcher has a directory `/home/user/datasets` containing several CSV files (with headers `x,y`). They need to fit a 1-dimensional Ordinary Least Squares (OLS) linear regression model ($y = mx + b$) to each dataset, evaluate the training Mean Squared Error (MSE), and organize the files based on the model's performance.

Your task is to write a C++ program and an accompanying shell script to perform the following:
1. Create the directories: `/home/user/organized/low_error` and `/home/user/organized/high_error`.
2. Write a C++ program (e.g., `pipeline.cpp`) that reads a CSV file containing `x` and `y` columns.
3. The C++ program must calculate the OLS weights `m` (slope) and `b` (intercept), and then calculate the `MSE` (Mean Squared Error) for the dataset. 
   - Use standard OLS formulas: 
     $m = \frac{n \sum(xy) - \sum x \sum y}{n \sum(x^2) - (\sum x)^2}$
     $b = \frac{\sum y - m \sum x}{n}$
4. Your pipeline must evaluate each CSV file in `/home/user/datasets`.
5. Write the results for each file to a summary file at `/home/user/organized/metrics.txt`. The lines should be sorted alphabetically by filename and exactly match this format:
   `[filename]: m=[m], b=[b], MSE=[MSE]`
   *(Note: Format `m`, `b`, and `MSE` strictly to 4 decimal places).*
6. Move the original CSV files into `/home/user/organized/low_error/` if their $MSE < 1.0$, and into `/home/user/organized/high_error/` if their $MSE \ge 1.0$.

Ensure your C++ code handles standard compilation (e.g., `g++ -O2`) and only uses standard libraries. You are responsible for fully automating the execution of this pipeline.