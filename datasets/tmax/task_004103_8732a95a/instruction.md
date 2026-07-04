You are a Machine Learning Engineer responsible for preparing training data for a predictive model. The data preparation pipeline relies on a legacy, proprietary C executable located at `/app/preprocess_bin`. 

Recently, you noticed severe degradation in model reproducibility. After some debugging, you suspect that `/app/preprocess_bin` is silently corrupting the training data. Specifically, under certain statistical conditions, it silently converts valid floating-point values into `NaN`s in its output, destroying the downstream pipeline.

Your investigation suggests that this bug is triggered by specific properties of the input features—likely related to the correlation or covariance between the first two columns of the input data (X and Y). 

Your task is to:
1. **Analyze the Black Box:** Use standard Linux CLI tools and statistical reasoning to test `/app/preprocess_bin` against the provided sample datasets in `/app/sample_data/`. Determine the exact statistical threshold (involving correlation/covariance) that triggers the silent `NaN` corruption. 
2. **Build a Sanitizer:** Write a C program that acts as a gatekeeper for the pipeline. It must read an input CSV, compute the necessary statistics, and decide whether the file is safe to process.
3. **Compile:** Save your code at `/home/user/validate_dataset.c` and compile it to `/home/user/validate_dataset`.

**Program Specifications (`validate_dataset`):**
*   **Input:** The program will receive the path to a CSV file as its first command-line argument (e.g., `./validate_dataset data.csv`).
*   **File Format:** The CSVs have a header row and three columns of floating-point numbers (`X,Y,Z`). 
*   **Output Behavior:** 
    *   If the file is "safe" (will NOT trigger the `NaN` corruption in `/app/preprocess_bin`), the program must exit with **exit code 0**.
    *   If the file is "evil" (WILL trigger the `NaN` corruption), the program must exit with **exit code 1**.
    *   You may print anything to `stdout` or `stderr`; the automated verifier will only check the exit code.

**Constraints & Hints:**
*   You must implement the statistical calculation (e.g., Pearson correlation coefficient or covariance) from scratch in C. Standard libraries (`math.h`, `stdio.h`, `stdlib.h`, `string.h`) are allowed.
*   The threshold triggering the bug is a clean, standard numerical cut-off.
*   You can run `/app/preprocess_bin <input.csv> <output.csv>` to observe its behavior on the sample data.