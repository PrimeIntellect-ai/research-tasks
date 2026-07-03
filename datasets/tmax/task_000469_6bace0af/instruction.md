You are a researcher organizing and migrating legacy datasets. As part of this effort, you need to replace an old, undocumented data-processing tool with a maintainable C++ pipeline. 

The legacy tool is located at `/app/stat_oracle` (a stripped Linux binary). It takes a single command-line argument: the path to a CSV file. 
The input CSVs always have a header row and the following columns: `id,group,val_A,val_B`.
The `group` column contains either the string `control` or `treatment`.

Through some initial investigation, we know the legacy tool performs the following high-level steps:
1. **Data Cleaning (ETL):** It filters out certain invalid rows based on simple rules applied to `val_A` and `val_B`.
2. **Feature Engineering:** It computes a new derived feature linearly combining `val_A` and `val_B`.
3. **Statistical Modeling:** It computes the **Welch's t-statistic** for the derived feature, comparing the `treatment` group against the `control` group (i.e., `mean_treatment - mean_control` in the numerator).
4. **Reporting:** It prints the resulting t-statistic to standard output as a floating-point number.

Your task is to write a C++ program at `/home/user/repl.cpp` that perfectly mimics the behavior of the legacy tool. 
- Compile your program to an executable located at `/home/user/repl`.
- Like the oracle, `/home/user/repl` must accept the CSV file path as its first command-line argument and print the computed t-statistic to stdout.
- You will need to interact with the `/app/stat_oracle` binary, feeding it mock datasets to reverse-engineer the exact filtering rules and the formula for the derived feature. 

An automated test will run both your compiled `/home/user/repl` and the `/app/stat_oracle` on a hidden suite of newly generated CSV files. To pass, the Maximum Absolute Error (MAE) between your program's outputs and the oracle's outputs must be less than `1e-4`.