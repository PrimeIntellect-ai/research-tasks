You are a Machine Learning Engineer tasked with preparing a clean dataset, reconstructing an undocumented PyTorch model architecture, and running a reproducible inference pipeline. 

You have been provided with a workspace directory at `/home/user/workspace/` containing the following files:
1. `/home/user/workspace/raw_data.csv`: A raw dataset containing features `f1`, `f2`, `f3`, `f4`, and `f5`. Some rows contain corrupted, missing, or out-of-bounds data.
2. `/home/user/workspace/model_weights.pth`: A saved PyTorch `state_dict`. The original model class is lost, so you must reconstruct it.
3. `/home/user/workspace/schema.json`: A JSON file defining the strict validation rules for the features.

Your objective is to complete the following steps:

**Phase 1: Data Schema Enforcement**
Write a script to parse `raw_data.csv` and enforce the rules defined in `schema.json`. 
- Discard any row containing null values.
- Discard any row where feature values fall outside the allowed `min` and `max` bounds specified in the schema.
- Discard any row where the data type cannot be cast to a standard float.
- Save the perfectly cleaned data to `/home/user/workspace/cleaned_data.csv` with the exact same column headers.

**Phase 2: Model Architecture Reconstruction**
Inspect the keys and tensor shapes inside `model_weights.pth`. Based on the `state_dict` keys (e.g., layers, weight/bias dimensions), reconstruct the exact PyTorch `nn.Module` architecture. 
Write your class definition in `/home/user/workspace/model.py`. The model must successfully load the provided `state_dict` without `strict=False`. 
*Hint:* It is a simple multi-layer perceptron (Feed-Forward Network) using `ReLU` activations between hidden layers. The final output has no activation.

**Phase 3: Pipeline Reproducibility Testing & Inference**
Write a script `/home/user/workspace/infer.py` that:
1. Loads the cleaned dataset (`cleaned_data.csv`).
2. Loads your reconstructed model and the weights.
3. Sets the model to evaluation mode (`.eval()`).
4. Performs inference on the cleaned features (as a single batch or row-by-row) using `torch.no_grad()`.
5. Outputs the predictions to `/home/user/workspace/predictions.csv`. This file should have a single column named `prediction` containing the exact float output for each corresponding row in `cleaned_data.csv`.

**Phase 4: Reporting**
Create a summary log file at `/home/user/workspace/summary.txt` containing exactly two lines in this format:
```
VALID_ROWS: <number_of_rows_in_cleaned_data>
SUM_PREDICTIONS: <sum_of_all_predictions_rounded_to_4_decimal_places>
```
Make sure you install any necessary Python packages (like `pandas`, `torch`) to complete this task.