You are a data engineer debugging an ETL pipeline written in C. 

We have a data processing pipeline that performs a crucial preprocessing step: Mean Centering, which is the first step of our dimensionality reduction pipeline. 
Currently, the program `/home/user/etl_processor.c` reads a dataset `/home/user/data.csv` (10,000 rows, 5 columns of floating-point numbers), calculates the mean for each column across the **entire** dataset, and then subtracts this mean from every row, writing the result to `/home/user/output.csv`.

However, we have a critical "data leakage" bug! In machine learning pipelines, statistics like the mean must be calculated *only* on the training data, and then applied to both the training and testing data. 

Your tasks:
1. Modify `/home/user/etl_processor.c` to compute the column means using **only the first 8,000 rows** (the training set).
2. Subtract this training mean from **all 10,000 rows** (both training and testing sets).
3. Ensure the output is formatted as comma-separated values with exactly 5 decimal places (e.g., `%.5f`).
4. Compile your fixed code into an executable named `/home/user/etl_processor`.
5. Run the executable so that it produces the corrected output at `/home/user/fixed_output.csv`.

Do not change the number of rows or columns in the output; the final file must have 10,000 rows and 5 columns. Ensure all system libraries needed for basic C compilation and math (`gcc`, `<stdio.h>`, `<stdlib.h>`) are utilized correctly.