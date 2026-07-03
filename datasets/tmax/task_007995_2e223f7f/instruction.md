You are an ML engineer tasked with preparing and evaluating cross-validation results from a custom C-based modeling pipeline. You have a raw dataset of model predictions stored at `/home/user/predictions.csv`. 

The CSV file contains the following columns (with a header row):
`run_id,fold,alpha,y_true,y_pred`

Where:
- `run_id`: An integer representing a specific tracking run.
- `fold`: An integer (1 to 5) representing the cross-validation fold.
- `alpha`: A floating-point hyperparameter used for that run.
- `y_true`: The actual target value (float).
- `y_pred`: The predicted value (float).

Your task is to write a C program at `/home/user/evaluate.c` that performs tabular data aggregation and model output validation to identify the best hyperparameter.

Specifically, the C program must:
1. Parse the CSV file `/home/user/predictions.csv`.
2. Compute the Mean Squared Error (MSE) for each unique `alpha` value across all folds combined.
3. Identify the `alpha` value that yields the lowest overall MSE.
4. Write the results to an experiment tracking log file at `/home/user/best_model.log`.

The output file `/home/user/best_model.log` must have EXACTLY the following format:
```
Best Alpha: <alpha_value_formatted_to_2_decimal_places>
Lowest MSE: <mse_value_formatted_to_4_decimal_places>
```

Requirements:
- You must write the solution in standard C. 
- You may use `<math.h>` and compile with `gcc -O2 evaluate.c -o evaluate -lm`.
- Run your compiled executable so that the `/home/user/best_model.log` file is successfully created.