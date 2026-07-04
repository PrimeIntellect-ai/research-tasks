You are an analyst tasked with building a high-performance data processing pipeline in C. You have two datasets located in your home directory:
1. `/home/user/users.csv` - Contains user demographics. Columns: `user_id,age`
2. `/home/user/activity.csv` - Contains user engagement metrics. Columns: `user_id,hours_active`

Your task is to write a C program that performs the following:
1. Reads and parses both CSV files.
2. Joins the datasets on the `user_id` field (inner join). You can assume the IDs perfectly match and are in the same order for simplicity, but your code should handle extracting the paired `age` and `hours_active` values.
3. Computes the Pearson correlation coefficient between `age` and `hours_active` across all matched users.
4. Writes the final correlation result to a tracking file at `/home/user/correlation_result.txt` in the exact format: `Correlation: X.XXXX` (rounded to 4 decimal places).

Steps:
1. Write the C code to `/home/user/compute_corr.c`.
2. Compile the code (remember to link the math library if necessary).
3. Run the compiled executable.

Constraints:
- Do not use any external libraries other than the standard C library (`stdio.h`, `stdlib.h`, `string.h`, `math.h`, etc.).
- Both CSVs have a header row which you must ignore.
- Ensure the output file `/home/user/correlation_result.txt` contains exactly the single line requested.