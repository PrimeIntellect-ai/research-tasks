You are a Data Engineer tasked with fixing and optimizing a C-based mathematical ETL pipeline.

We have a dataset of 100,000 records in `/home/user/data.csv` with the following columns:
`ID, Feature1, Feature2, Target`

The `ID` is a large 64-bit integer (e.g., `8000000000000000001`).
Our pipeline is designed to find the optimal smoothing hyperparameter $\alpha$ (between 0.00 and 1.00, step 0.01) for a simple predictive model:
$Prediction = \alpha \times Feature1 + (1 - \alpha) \times Feature2$

To ensure reproducibility, the pipeline uses 5-fold cross-validation. A record is assigned to a validation fold based on its ID: `Fold_Index = ID % 5`.

However, the previous engineer made a severe mistake in data schema enforcement. They stored the `ID` as a 32-bit `float` in the C struct. Because of floating-point precision loss on large integers, the IDs are silently corrupted during parsing. This causes the modulo operation `ID % 5` to map almost all records to the same fold, ruining the cross-validation splits and causing inaccurate hyperparameter tuning.

Your tasks are:
1. Examine the source code at `/home/user/etl_pipeline.c`.
2. Fix the data schema enforcement bug: change the `id` field to an `unsigned long long` and update the parsing logic so that 64-bit integers are read exactly without precision loss.
3. Ensure the cross-validation assignment `record.id % 5` is evaluated on the exact 64-bit integer ID.
4. Compile your fixed C program (using `gcc -O3 etl_pipeline.c -o etl_pipeline`).
5. Run the pipeline. The program is designed to test $\alpha$ from 0.00 to 1.00 and print the $\alpha$ that yields the lowest Mean Squared Error (MSE) across the validation folds.
6. Save the final output of the fixed program into `/home/user/report.txt`.

The output file `/home/user/report.txt` must strictly contain a single line in this format:
`Optimal alpha: X.XX, Best CV MSE: Y.YYYYYY`
(where X.XX is the best alpha, and Y.YYYYYY is the corresponding MSE rounded to 6 decimal places).

Do not change the random seed or the core mathematical logic for computing MSE. Only fix the data type, parsing, and schema bugs.