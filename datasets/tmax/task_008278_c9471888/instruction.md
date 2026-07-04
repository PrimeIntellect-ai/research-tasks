You are an AI assistant helping a data science researcher organize and process a dataset of sensor readings.

The researcher has a file located at `/home/user/raw_sensors.txt` containing messy, semi-structured log lines. 

Your task is to build a mini ETL pipeline, perform dimensionality reduction, and test numerical accuracy across data types. 

Please perform the following steps:

1. **ETL Extraction**: 
   Extract the 4 numerical features from `/home/user/raw_sensors.txt`. The file has lines in the format: `[INFO] MSG_ID=X : F1=<val> | F2=<val> | F3=<val> | F4=<val>`.
   Write these extracted features as comma-separated values (no headers) to `/home/user/features.csv`.

2. **Dimensionality Reduction (C Program)**:
   Write a C program at `/home/user/dim_reduce.c` that reads `/home/user/features.csv`.
   Project the 4D data down to 2D using the following fixed transformation:
   - `PC1 = 0.5 * F1 + 0.5 * F2 + 0.5 * F3 + 0.5 * F4`
   - `PC2 = 0.5 * F1 - 0.5 * F2 + 0.5 * F3 - 0.5 * F4`
   
   The C program must perform this entire process *twice* internally:
   - Once using single-precision (`float`) for all parsing, calculations, and storage.
   - Once using double-precision (`double`) for all parsing, calculations, and storage.
   
   Output the results to `/home/user/projected_float.csv` and `/home/user/projected_double.csv` respectively. Both files should have lines formatted with 6 decimal places (e.g., `%.6f,%.6f`).

3. **Numerical Accuracy Testing**:
   Compare the values in `/home/user/projected_float.csv` and `/home/user/projected_double.csv`. Find the maximum absolute difference between the two precision outputs across all values (checking every PC1 and PC2 pair for every row).
   Write this single maximum difference (formatted to exactly 8 decimal places) to `/home/user/max_error.txt`.

Ensure your C program compiles with `gcc -O3 -o /home/user/dim_reduce /home/user/dim_reduce.c`. Execute your pipeline so that all target output files exist in `/home/user/` when you finish.