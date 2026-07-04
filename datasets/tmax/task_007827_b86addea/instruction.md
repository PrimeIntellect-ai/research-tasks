I am a researcher organizing experimental datasets for a regression task. I have a large dataset of ground truth values and predictions from two different models (Model Alpha and Model Beta). Currently, my Go-based pipeline is broken—it's producing empty evaluations, similar to a plotting script that renders blank charts due to misconfiguration. 

I need you to build a robust Go-based ETL and evaluation pipeline that calculates cross-validation metrics (Mean Squared Error) and includes strict numerical accuracy tests.

**Workspace details:**
All work should be done in `/home/user/evaluation_pipeline/`.
I have provided three files in `/home/user/data/` (you will need to read these):
1. `ground_truth.csv`: Contains `id`, `fold_id`, and `true_value`. (`fold_id` ranges from 1 to 5).
2. `preds_alpha.csv`: Contains `id` and `pred_value` for Model Alpha.
3. `preds_beta.csv`: Contains `id` and `pred_value` for Model Beta.

**Your Tasks:**

1. **ETL & Evaluation Go Program (`main.go`)**
   Write a Go program in `/home/user/evaluation_pipeline/main.go` that:
   - Reads the three CSV files efficiently (assume they could be large, though these are samples).
   - Joins the predictions to the ground truth using the `id` column.
   - Calculates the Mean Squared Error (MSE) for both Model Alpha and Model Beta for each `fold_id`.
   - Calculates the average cross-validation MSE across all 5 folds for each model.
   - Determines the `best_model` (the one with the lowest average MSE).
   - Writes the results to `/home/user/evaluation_pipeline/results.json`.

   The JSON must *exactly* match this structure:
   ```json
   {
     "alpha": {
       "fold_1_mse": 0.0000,
       "fold_2_mse": 0.0000,
       "fold_3_mse": 0.0000,
       "fold_4_mse": 0.0000,
       "fold_5_mse": 0.0000,
       "average_mse": 0.0000
     },
     "beta": {
       "fold_1_mse": 0.0000,
       "fold_2_mse": 0.0000,
       "fold_3_mse": 0.0000,
       "fold_4_mse": 0.0000,
       "fold_5_mse": 0.0000,
       "average_mse": 0.0000
     },
     "best_model": "alpha"
   }
   ```
   *(Note: Format all float values in the JSON to 4 decimal places, e.g., using `math.Round(val*10000)/10000` or custom JSON marshaling).*

2. **Numerical Accuracy Testing (`math_test.go`)**
   Create a test file `/home/user/evaluation_pipeline/math_test.go` that tests your MSE calculation function. 
   - Write at least two unit tests validating the numerical accuracy of your MSE function against known inputs (e.g., testing that an array of exact matches returns 0.0, and testing a known standard case).
   - Ensure `go test` runs successfully in the `/home/user/evaluation_pipeline/` directory.

Run your program to generate the `results.json` file. Ensure `go mod init evaluation_pipeline` is initialized so the tests run properly.