You are acting as a Data Engineer. We have a data processing pipeline written in Go that applies Z-score normalization (Standard Scaler) to our dataset prior to a dimensionality reduction step.

Unfortunately, our current implementation suffers from **data leakage**. The script computes the mean and sample standard deviation across the *entire* dataset (both 'train' and 'test' splits) and then scales all rows. This leaks information from the test set into the training transformations.

Your task is to fix the Go program located at `/home/user/csv_processor/main.go`.

**Requirements:**
1. Analyze `main.go` and identify where the mean and standard deviation are calculated.
2. Modify the logic so that the mean and sample standard deviation (using $n-1$) are calculated **only** using the rows where the `Split` column equals `"train"`.
3. Use these `train`-derived statistics to scale **all** rows in the dataset (both `"train"` and `"test"`).
4. Save your modified code and execute it to generate the output file at `/home/user/csv_processor/processed.csv`.
5. The output CSV must have the exact same header as the input, with the scaled features rounded/formatted to 4 decimal places (e.g., `45.0000`).
6. Do not change the order of the rows.

**Environment details:**
- Working directory: `/home/user/csv_processor`
- Input dataset: `/home/user/csv_processor/dataset.csv`
- The Go module is already initialized. You can build and run using standard `go run main.go` or `go build`.

Ensure your final `processed.csv` accurately reflects the test set scaled strictly by the training distribution.