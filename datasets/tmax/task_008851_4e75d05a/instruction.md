You are an ETL engineer tasked with cleaning a raw data feed and selecting the best mathematical model for a data pipeline.

A raw CSV file will be located at `/home/user/dataset.csv`. It contains three columns: `id`, `x`, and `y`.

However, the dataset contains corrupted rows. In some cases, `x` or `y` are empty strings, "NaN", or non-numeric characters. A common pitfall in C pipelines is using standard conversion functions like `atof` which silently convert invalid strings or empty values to `0.0`. This will ruin the model inference.

Your task is to write a C program `/home/user/etl_infer.c` that does the following:
1. **Data Schema Enforcement:** Parse the CSV and strictly enforce the schema. You must drop any row where `x` or `y` is missing, empty, or fails to be a strictly valid float.
2. **Model Architecture Reconstruction & Inference:** For the *cleaned* rows, compute the predictions ($\hat{y}$) for three candidate polynomial models:
   * **Model 1 (Linear):** $\hat{y} = 1.5 + 2.0x$
   * **Model 2 (Quadratic):** $\hat{y} = -0.5 + 1.2x + 0.5x^2$
   * **Model 3 (Cubic):** $\hat{y} = -0.5 + 1.2x + 0.5x^2 - 0.1x^3$
3. **Cross-validation / Evaluation:** Calculate the Mean Squared Error (MSE) for each of the three models on your cleaned dataset.
   * $MSE = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$ (where $N$ is the number of valid rows).

Finally, determine which model has the lowest MSE. Write the ID of the best model and its MSE to a file named `/home/user/best_model.txt` exactly in the following format (rounding the MSE to 4 decimal places):

`Model: <id>, MSE: <mse>`

**Constraints:**
* You must use **C** as the primary language to parse the CSV, compute the inferences, and output the result. 
* Compile your code to an executable at `/home/user/etl_infer` and run it to produce the final output.