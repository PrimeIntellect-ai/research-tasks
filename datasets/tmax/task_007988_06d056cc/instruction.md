You are an AI assistant helping a data engineer build a robust ETL pipeline in C. 

We have a dataset of 3D token embeddings in a CSV file located at `/home/user/data.csv`. The file has no header and contains 5 columns: `token_id`, `token_string`, `x`, `y`, `z`.

Due to upstream extraction errors, some of the coordinate values (`x`, `y`, or `z`) are missing and represented as the exact string `"NaN"`. A common trap in C is that using `atof()` or `sscanf()` on `"NaN"` might silently evaluate to `0.0` or another fallback value, causing silent data corruption similar to what happens in poorly configured pandas pipelines.

Your task is to write and execute a C program at `/home/user/process.c` that does the following:
1. Opens and reads `/home/user/data.csv`.
2. Tokenizes the lines to parse the columns.
3. Strictly **ignores and skips** any row where `x`, `y`, or `z` is exactly the string `"NaN"`.
4. Computes the magnitude (Euclidean norm) of the 3D embedding vector $(x, y, z)$ for each valid row.
5. Computes the sample mean ($\bar{x}$) and the 95% confidence interval of the mean for these magnitudes. Use the formula $CI = \bar{x} \pm 1.96 \times \frac{s}{\sqrt{n}}$, where $s$ is the sample standard deviation (with Bessel's correction, i.e., dividing by $n-1$).
6. Writes the results to a file at `/home/user/output.txt` in exactly this format:
   `Mean: <mean>, CI: [<lower>, <upper>]`
   (Round the floating-point numbers to exactly 4 decimal places).

Please write the code, compile it (you can name the executable `/home/user/process`), and run it to produce the `output.txt` file. Standard C libraries are available.