You are an MLOps engineer tasked with validating the outputs of several recently trained regression models. 

You have a directory containing experiment artifacts at `/home/user/experiments/`. Inside this directory, there are multiple CSV files, each named after a specific model version (e.g., `model_A.csv`, `model_B.csv`). Each CSV file contains the prediction results of a model on a validation dataset, with the columns:
- `id`: The identifier of the sample
- `y_true`: The ground truth value
- `y_pred`: The model's predicted value

Your task is to write a Python script (and execute it) to perform the following:
1. Iterate over all CSV files in `/home/user/experiments/`.
2. Load the tabular data and strictly cast the `y_true` and `y_pred` arrays to `numpy.float32` (this numerical configuration step is required to simulate a specific lower-precision hardware deployment).
3. Calculate the Mean Squared Error (MSE) for each model using the `float32` arrays.
4. Validate the models by filtering out any model that has an MSE strictly greater than or equal to `0.5`.
5. Aggregate the passing models and save the results to a new file at `/home/user/valid_models.csv`.

The output file `/home/user/valid_models.csv` must:
- Have exactly two columns with headers: `model_name,mse`
- The `model_name` should be the filename without the `.csv` extension (e.g., `model_A`).
- The `mse` should be formatted to exactly 4 decimal places (e.g., `0.1250`).
- Be sorted in ascending order of MSE.

Write the necessary code, run it, and ensure the final CSV is correctly formatted and located at the requested path.