You are acting as a data analyst. We have a batch of 3D coordinate data in a CSV file located at `/home/user/points.csv`. We need to run a fast linear classification on this data using C to ensure maximum performance.

Your task is to create a reproducible pipeline that processes this CSV file, enforces a strict schema, applies a linear classification model, and outputs the results.

Requirements:
1. Write a C program named `/home/user/classifier.c`.
2. The C program must read `/home/user/points.csv`.
   - The CSV has a header: `id,x,y,z`
   - Valid rows have an integer `id` and floating-point values for `x`, `y`, and `z`.
   - **Schema Enforcement**: Any row that does not strictly contain exactly 4 comma-separated values, or has non-numeric/empty fields for the coordinates, must be completely ignored (skipped).
3. For each valid row, compute the classification score using the linear weights: 
   $W = [0.5, -0.2, 0.1]$ and bias $b = -0.5$.
   The score formula is: $score = (0.5 \times x) + (-0.2 \times y) + (0.1 \times z) - 0.5$
   - If $score > 0$, the predicted class is `1`.
   - Otherwise, the predicted class is `0`.
4. The C program must output the predictions to a file named `/home/user/results.csv` with the header `id,class` and the corresponding integer values for each valid processed row.
5. Create an executable bash script named `/home/user/pipeline.sh` that:
   - Compiles `classifier.c` using `gcc` into an executable named `classifier`.
   - Executes `classifier`.

Ensure your C code handles standard file I/O safely and your pipeline script has the correct permissions to run.