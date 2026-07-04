As an MLOps engineer, you need to track how different hyperparameters correlate with model performance based on our unstructured experiment artifact logs. 

I have a log file located at `/home/user/experiment_logs.txt`. Each line in this file corresponds to a different training run and contains various metrics and parameters formatted in a semi-structured string.

Your task is to:
1. Write a C++ program (e.g., `analyze.cpp`) that reads and tokenizes `/home/user/experiment_logs.txt`.
2. Extract the Learning Rate (`LR`) and Validation Loss (`ValLoss`) as paired floating-point datasets. 
3. Compute the Pearson correlation coefficient between the Learning Rate (independent variable) and Validation Loss (dependent variable).
4. Save the computed correlation coefficient to a file named `/home/user/correlation.txt`. The output should contain strictly the numerical value formatted to exactly 4 decimal places (e.g., `0.1234` or `-0.1234`), followed by a newline.

Constraints:
- Use C++ as the primary programming language for the analysis logic. You can use standard bash commands to compile and execute your code.
- Only use the C++ Standard Library (do not rely on external packages like Boost).
- The parsing logic must correctly skip other metrics (like `Exp_ID`, `BS`, and `Acc`).

Compile your code, run the executable, and ensure the resulting `/home/user/correlation.txt` is created with the correct value.