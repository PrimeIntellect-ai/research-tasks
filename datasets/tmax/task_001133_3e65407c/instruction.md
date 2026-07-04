You are an open-source maintainer reviewing a PR for a numerical library. The PR attempts to implement a custom data structure for "Exact Online Simple Linear Regression", which maintains a rolling set of 2D integer points and allows querying predictions using exact rational arithmetic to avoid floating-point inaccuracies. 

The PR author provided a C++ reference implementation, which has been compiled as a stripped binary at `/app/linreg_ref`. However, the Python implementation they submitted at `/home/user/linreg.py` is broken, slow, and fails edge cases.

Your task is to fix the Python implementation and set up a CI script to verify it.

### Specifications for `/home/user/linreg.py`:
1. The script must read commands from standard input, one per line, and write results to standard output.
2. Supported commands:
   - `ADD <x> <y>`: Adds the integer point (x, y) to the dataset. Do not print anything.
   - `REMOVE_OLDEST`: Removes the oldest point added to the dataset that hasn't been removed yet. If the dataset is empty, print `ERROR`.
   - `PREDICT <x>`: Predicts the y-value for the given integer `<x>` using simple linear regression based on the current points. 
     - Formula: $y = \beta_0 + \beta_1 x$
     - $\beta_1 = \frac{n \sum (xy) - \sum x \sum y}{n \sum (x^2) - (\sum x)^2}$
     - $\beta_0 = \frac{\sum y - \beta_1 \sum x}{n}$
     - If the number of points $n < 2$, or if the variance of $X$ is exactly 0, print `ERROR`.
     - Otherwise, print the exact predicted y-value as an irreducible fraction in the format `numerator/denominator`. If the denominator is 1, just print the integer `numerator`. If the value is negative, the minus sign must be on the numerator.
3. The algorithm must process `ADD` and `REMOVE_OLDEST` in $O(1)$ time by maintaining running sums, rather than recalculating from scratch. Use exact rational arithmetic (e.g., Python's `fractions` module) to prevent precision loss.

### Specifications for CI setup:
Create a bash script at `/home/user/ci_test.sh` that:
1. Generates a random test file with 1000 valid commands.
2. Runs both `/app/linreg_ref` and `python3 /home/user/linreg.py` on this file.
3. Compares their outputs. If they match perfectly, exit with 0. If they differ, print the diff and exit with 1.

Ensure your Python script exactly matches the behavior of the black-box oracle `/app/linreg_ref` under all conditions.