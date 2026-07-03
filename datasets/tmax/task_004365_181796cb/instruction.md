You are a Data Analyst tasked with fixing a machine learning data pipeline written in C. 

The pipeline processes sensor readings and their corresponding labels. However, a junior analyst reported that our evaluation metrics look suspiciously good, suggesting a "data leak" where information from the test set is leaking into the training transformations.

Your environment contains the following directories and files:
- `/home/user/data/sensors.csv`: Contains sensor readings. Format: `id,val1` (no header, sorted by `id`).
- `/home/user/data/labels.csv`: Contains labels. Format: `id,label` (no header, sorted by `id`).
- `/home/user/normalize.c`: A C program that reads a joined dataset, normalizes the `val1` feature by subtracting the mean, and writes the output.

Your tasks are:
1. **Multi-source data joining**: Use standard Linux tools to join `/home/user/data/sensors.csv` and `/home/user/data/labels.csv` on the `id` column. Output the result to `/home/user/data/joined.csv`. The output format should be `id,val1,label` (comma-separated).
2. **Fix the Data Leak**: Inspect `/home/user/normalize.c`. It currently computes the mean of `val1` over the *entire* dataset. Modify the C code so that it calculates the mean using **only the first 80 rows** (our training split), but still applies this training mean to normalize **all** rows (train and test). 
3. **Build & Benchmark**: Compile the fixed C program into an executable at `/home/user/normalize` using `gcc`. Run the executable to produce `/home/user/predictions.csv` and `/home/user/mean_used.txt` (the C code already handles the file writing once compiled). Time the execution of the program.
4. **Experiment Tracking**: Create a summary file at `/home/user/report.txt` containing exactly two lines:
   - Line 1: The correct training mean used for normalization (read this from `/home/user/mean_used.txt`).
   - Line 2: The normalized `val1` value for the 81st row (id=81) in `/home/user/predictions.csv`.

Ensure your C code compiles without errors and properly processes the CSV files.