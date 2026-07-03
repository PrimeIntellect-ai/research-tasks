You are an ML engineer preparing a pipeline to process legacy sensor data. As part of the preprocessing step, the 3D sensor readings need to be projected into a 2D space for an older inference model. 

The projection matrix required for this dimensionality reduction was lost in text format, but a screenshot of the configuration is available at `/app/projection_matrix.png`. 

Your task is to:
1. Extract the projection matrix from the image `/app/projection_matrix.png`. You can use `tesseract` (which is pre-installed) to read the numerical values. The image contains exactly two lines of text, with three space-separated floats per line. This represents a 2x3 matrix (2 rows, 3 columns).
2. Write a Go program at `/home/user/reducer.go` that performs this dimensionality reduction.
3. The Go program must read lines from Standard Input (`stdin`). Each input line will contain exactly three comma-separated float64 values (representing a 3D vector `[x1, x2, x3]`).
4. For each input vector, multiply the 2x3 projection matrix by the 3x1 input vector to produce a 2x1 output vector `[y1, y2]`.
   - `y1 = (row1_col1 * x1) + (row1_col2 * x2) + (row1_col3 * x3)`
   - `y2 = (row2_col1 * x1) + (row2_col2 * x2) + (row2_col3 * x3)`
5. Ensure your numerical configuration is highly precise. Calculate the results using `float64`.
6. Output the resulting 2D vector to Standard Output (`stdout`) as two comma-separated values, formatted to exactly 4 decimal places (e.g., `fmt.Printf("%.4f,%.4f\n", y1, y2)`). 
7. Ignore any blank lines in the input. If EOF is reached, the program should exit gracefully with code 0.
8. Compile your Go program to an executable named `/home/user/reducer`.

Do not add any additional text, logging, or prompt characters to `stdout`. The output must strictly match the transformed data format so it can be cleanly piped into our inference benchmarking harness.