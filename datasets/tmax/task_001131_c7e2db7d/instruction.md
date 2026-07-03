You are a Machine Learning Engineer building a high-performance data preprocessing pipeline. You have a raw sensor dataset that needs to be cleaned extremely fast before being fed into a training loop, so you decide to write the core imputation and outlier handling logic in C.

Your task is to create a fully reproducible pipeline that compiles your C program and processes the data.

**Requirements:**

1. **Input Data**: A file located at `/home/user/signal.csv` containing a single column of floating-point numbers. Some rows are completely empty, and some contain the string `NaN` (representing missing values).
2. **C Program (`/home/user/cleaner.c`)**: Write a C program that reads `signal.csv` and outputs a cleaned version to `/home/user/clean_signal.csv`.
   - **Pass 1**: Calculate the arithmetic mean and the population standard deviation of all valid, numeric entries (ignore empty lines and `NaN`).
   - **Pass 2**: Iterate through the data again to generate the output:
     - If a value is missing (empty or `NaN`), replace it with the calculated mean.
     - If a value is an outlier (greater than `mean + 2.0 * std_dev` or less than `mean - 2.0 * std_dev`), cap it at exactly that upper or lower bound.
     - If a value is valid and not an outlier, keep it as is.
   - **Format**: All output numbers must be formatted to exactly 4 decimal places (e.g., `%.4f`), with one number per line.
3. **Pipeline Script (`/home/user/pipeline.sh`)**: Write a bash script that:
   - Installs any necessary standard C compiler tools if they are missing (assume Debian/Ubuntu base, e.g., `apt-get install -y gcc`).
   - Compiles `/home/user/cleaner.c` into an executable named `/home/user/cleaner` (make sure to link the math library).
   - Runs `/home/user/cleaner` to produce `/home/user/clean_signal.csv`.

Ensure your bash script is executable (`chmod +x /home/user/pipeline.sh`) and succeeds when run. The automated tests will run `/home/user/pipeline.sh` and then verify the exact contents of `/home/user/clean_signal.csv`.