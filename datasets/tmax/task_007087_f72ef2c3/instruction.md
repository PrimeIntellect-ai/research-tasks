You are an AI assistant helping a data analyst debug a data processing pipeline. 

The analyst is trying to compute store-level aggregations and a simple linear regression model (predicting `Sales` from `Customers`) using a C++ program. However, similarly to a misconfigured plotting library outputting blank plots, the C++ program currently outputs `NaN` (Not a Number) for all statistics. 

Here is the current state of the workspace:
- The raw dataset is located at `/home/user/data/raw_data.csv`. It contains 5 columns: `ID,Store_ID,Customers,Sales,Promo`.
- The dataset has a header row.
- Some rows have corrupted numerical fields containing the string `"NA"`.
- The C++ source code is located at `/home/user/analyze.cpp`. 

Your tasks are to:
1. **Data Cleaning (Bash):** Use standard bash utilities (e.g., `awk`, `grep`, `sed`) to create a cleaned version of the dataset at `/home/user/data/clean_data.csv`. The cleaned dataset must:
   - Retain the header row.
   - Completely remove any rows that contain the string `"NA"`.
2. **Code Debugging (C++):** Fix the bugs in `/home/user/analyze.cpp`. 
   - The program currently fails to skip the header row, which causes parsing errors that poison the numerical calculations with `NaN`.
   - Ensure the program correctly parses the CSV, computes the average `Sales` per `Store_ID`, and calculates the global linear regression slope coefficient (beta) predicting `Sales` from `Customers` using the formula: `beta = sum((x_i - mean_x) * (y_i - mean_y)) / sum((x_i - mean_x)^2)`.
3. **Compilation and Execution:** Compile the fixed C++ code using `g++` and run it against `/home/user/data/clean_data.csv`. The C++ program should output its results to `/home/user/results.txt`.
   - The format of `/home/user/results.txt` should be:
     ```
     Global Beta: <beta_value>
     Store 1 Avg Sales: <avg_sales>
     Store 2 Avg Sales: <avg_sales>
     ...
     ```
     (Print values to 2 decimal places).
4. **Testing Pipeline:** Write a bash test script at `/home/user/verify_results.sh` that checks if `/home/user/results.txt` exists, ensures no `NaN` values are present in the file, and exits with code `0` if successful, or `1` otherwise. Make it executable.

Ensure all outputs strictly follow the specified file paths and formats.