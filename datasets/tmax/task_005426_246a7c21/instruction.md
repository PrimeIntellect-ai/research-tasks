You are acting as a data scientist working on an edge-computing device. We need to clean and aggregate a stream of sensory datasets using Go. 

There is a local, vendored copy of the `gonum` math library located at `/app/gonum`. We do not have internet access to download new modules, so you must use this local copy. However, a junior engineer accidentally introduced a syntax error into `/app/gonum/stat/stat.go` recently. 

Your task is to:
1. Find and fix the syntax error in the vendored `gonum` package at `/app/gonum/stat/stat.go`.
2. Write a Go program at `/home/user/process.go` that reads CSV data from `stdin` and writes a JSON array to `stdout`.
3. Compile your program to an executable at `/home/user/process`.

The CSV data read from `stdin` will have a header row: `category,x,y,z`.
Your Go program must perform the following pipeline:
- **Tabular Transformation & Cleaning:** Read the CSV. Skip any rows where `x`, `y`, or `z` cannot be parsed as standard floating-point numbers or are empty.
- **Dimensionality Reduction:** Project the 3D data (`x`, `y`, `z`) onto a 1D score using fixed static weights: `score = 0.5*x + 0.3*y + 0.2*z`.
- **Hypothesis Testing / Confidence Intervals:** Group the data by `category`. For each category, compute the Mean and the 95% Confidence Interval for the mean of the `score`. Use the standard normal approximation: `CI = Mean ± 1.96 * (StdDev / sqrt(N))`. Use the sample standard deviation (Bessel's correction, N-1). If a category has fewer than 2 valid rows, omit it from the output entirely.
- **Formatting:** Print a JSON array of objects to `stdout`. Each object must have the keys `"category"` (string), `"mean"` (float), `"ci_lower"` (float), and `"ci_upper"` (float). 
- **Sorting & Precision:** Sort the JSON array alphabetically by `"category"`. Round the `mean`, `ci_lower`, and `ci_upper` to exactly 4 decimal places.

Make sure your program correctly references the local `/app/gonum` module using a `replace` directive in your `go.mod`. Ensure the final executable is located exactly at `/home/user/process`.