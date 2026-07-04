You are tasked with cleaning a noisy dataset and applying dimensionality reduction using Go. 

We have collected sensor data into a CSV file located at `/app/data.csv`. The dataset has four features: `F1`, `F2`, `F3`, and `F4`. Unfortunately, the data has missing values and outliers. 

We also have a scanned image of the laboratory's data quality guidelines at `/app/guidelines.png`. 

Your goal is to write a Go program (in `/home/user/workspace/`, you will need to initialize the go module yourself) that does the following:

1. **Extract Guidelines**: Use standard OCR tools (like `tesseract`, which is installed on your system) to read `/app/guidelines.png` and find the outlier exclusion thresholds, imputation strategy, and the target number of dimensions for PCA.
2. **Handle Missing Values and Outliers**:
   - Parse `/app/data.csv`. 
   - Drop any rows that violate the outlier thresholds extracted from the image.
   - For the remaining rows, impute any missing (empty) values using the specified imputation strategy from the image (calculated over the valid, non-missing values of that column after outlier removal).
3. **Covariance and PCA (Dimensionality Reduction)**:
   - Mean-center the cleaned, imputed data.
   - Compute the covariance matrix of the centered data.
   - Perform Principal Component Analysis (PCA) to reduce the dataset to the target number of dimensions specified in the guidelines. Use the `gonum.org/v1/gonum` library for matrix operations and eigenvalue decomposition.
4. **Reconstruct Data**:
   - Project the reduced data back into the original 4-dimensional space (i.e., reconstruction using only the top principal components). Add the column means back to the reconstructed data.
5. **Output**:
   - Save the reconstructed dataset as `/home/user/reconstructed.csv`. The CSV should have no header, and exactly 4 columns of floating-point numbers formatted to 6 decimal places, separated by commas. The row order must exactly match the row order of the *cleaned* dataset (after outlier rows were dropped).

**Important Constraints**:
- Use Go as your primary programming language for the data processing.
- You may use bash tools to investigate the image and files.