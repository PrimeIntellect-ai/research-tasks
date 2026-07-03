You are an MLOps engineer troubleshooting a pipeline failure. A C program, `artifact_analyzer.c`, is designed to read experiment artifacts (a serialized weights matrix) and compute summary statistics. Currently, it produces incorrect, garbage metrics.

The artifact file is located at `/home/user/weights.bin`. It contains a flattened 100x100 matrix of weights. 

The program is supposed to:
1. Enforce the correct data schema: Read the binary data. The upstream model actually serializes the weights as 64-bit IEEE 754 floating-point numbers (`double`), but the current C code mistakenly reads them as 32-bit `float`.
2. Compute the mean of all elements in the matrix.
3. Compute the population standard deviation ($\sigma$) of the elements.
4. Compute the 95% Confidence Interval for the mean using the Z-distribution ($Z = 1.96$). The margin of error is $1.96 \times (\sigma / \sqrt{n})$.
5. Output the results to `/home/user/artifact_metrics.json` in the exact following format:
   `{"mean": <value>, "ci_lower": <value>, "ci_upper": <value>}` (formatted to 6 decimal places).

Your task:
1. Fix the schema mismatch (change the data type read from the file to `double`).
2. Fix any mathematical bugs in the variance/standard deviation calculation within the C code.
3. Compile the fixed C code.
4. Run the executable to generate the corrected `/home/user/artifact_metrics.json`.

The buggy code is located at `/home/user/artifact_analyzer.c`. You may use `gcc` to compile it.