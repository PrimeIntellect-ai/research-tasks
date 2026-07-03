You are acting as a data analyst. We have a raw dataset located at `/app/data.csv` containing numerical features across 10 columns. 

Recently, a colleague tried to generate a visualization of this data but misconfigured their plotting backend, resulting in a mostly blank image saved at `/app/plot_config.png`. However, the title and a small text annotation in the image are still visible and contain the required preprocessing instructions.

Your tasks are:
1. Read the text from the image `/app/plot_config.png` to find the exact scaling method and the target number of dimensions for dimensionality reduction.
2. Write a Go program (save it as `/app/reduce.go`) that:
   - Parses `/app/data.csv`.
   - Applies the feature scaling method specified in the image.
   - Performs Principal Component Analysis (PCA) to reduce the data to the target number of dimensions specified in the image.
   - Projects the scaled data onto the principal components (ordered by descending eigenvalues).
   - Saves the projected data as a CSV file to the output path specified in the image (no header, comma-separated, format floats with `%f`).
3. Run your Go program to generate the output CSV.

You may use standard Linux tools (like `tesseract` for OCR) and third-party Go packages like `gonum.org/v1/gonum` to perform the matrix operations and eigendecomposition. 
Ensure your Go environment is properly initialized.

Your final output must exactly match the expected mathematical projection (up to a small floating-point tolerance).