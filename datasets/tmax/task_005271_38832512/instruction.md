You are acting as a data analyst, but you need to process a dataset using C because of environment restrictions. 

You have a CSV file located at `/home/user/data.csv` with the following columns: `id,group,score`.
Some rows have missing `score` values, represented by an empty string (e.g., `3,A,` or `id,group,,`). If parsed naively with functions like `atoi`, these empty fields might silently convert to `0`, corrupting the analysis.

Your task is to write a C program that calculates the 95% confidence interval for the mean `score` of group `A`.

Write and compile a C program at `/home/user/analyze.c` (compiled to `/home/user/analyze`) that does the following:
1. Opens and reads `/home/user/data.csv`.
2. Tokenizes the CSV lines.
3. Filters for rows where `group` is exactly the string `A`.
4. Extracts the `score` as a floating-point number. You must carefully skip any rows where the `score` is missing (empty).
5. Calculates the sample mean and the sample standard deviation (using `n-1` degrees of freedom) for the valid group `A` scores.
6. Calculates the 95% confidence interval for the mean. Use the normal approximation with z = 1.96. The formula for the margin of error is `1.96 * (sample_std_dev / sqrt(n))`.
7. Writes the final result to a file named `/home/user/result.txt` in the exact following format (using `%.2f` for all floating point values):
`Mean: <mean>, CI: [<lower>, <upper>]`

Constraints:
- Only use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, `math.h`).
- Make sure to link the math library (`-lm`) when compiling.
- Assume the maximum line length in the CSV is 256 characters.
- Skip the header row.