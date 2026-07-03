You are a data scientist working on cleaning and validating a dataset using shell scripting. 

You have been provided with a dataset at `/home/user/dataset.csv` and a pre-written Python model script at `/home/user/model.py`. The model script performs dimensionality reduction and Bayesian inference natively, but it requires an orchestrator to handle the sampling, cross-validation routing, and model output validation.

Write a Bash script at `/home/user/run_pipeline.sh` that performs the following steps:

1. **Bootstrap Sampling**: 
   Read `/home/user/dataset.csv` (which has a header and 100 data rows). Generate a bootstrap sample (random sampling *with replacement*) of exactly 50 data rows from the original dataset. Save this to `/home/user/bootstrap_sample.csv`. (Do not include the header in the output).

2. **Cross-Validation Implementation**:
   Implement a manual 5-fold cross-validation routine in Bash on the data rows of `/home/user/dataset.csv`.
   - Split the 100 data rows into 5 equal, consecutive folds (20 rows each: rows 1-20 are fold 1, 21-40 fold 2, etc.).
   - Iterate 5 times. In each iteration `i` (from 1 to 5):
     - Create a test set containing the 20 rows for fold `i`.
     - Create a training set containing the remaining 80 rows.
     - Execute the model: `python3 /home/user/model.py --train <train_file> --test <test_file> --pca`
     - The script will output a single line like `Accuracy: 0.XX`. Capture this value.

3. **Model Output Validation**:
   Calculate the average accuracy across all 5 folds. 
   Write ONLY the final average accuracy (formatted to 2 decimal places, e.g., `0.85`) to `/home/user/final_metric.txt`.

Ensure your script is executable (`chmod +x /home/user/run_pipeline.sh`) and runs without errors. You may create temporary files in `/home/user/` as long as you clean them up or leave them; only `bootstrap_sample.csv` and `final_metric.txt` are strictly verified.