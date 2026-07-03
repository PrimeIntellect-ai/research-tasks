You have been given a machine learning pipeline script at `/home/user/pipeline.py` and a dataset directory `/home/user/data/` containing `train.csv` and `test.csv`. 

The pipeline is supposed to train a Random Forest classifier using a few numerical features and one high-cardinality discrete feature (`device_id`). The target variable is `target`. 

Currently, the pipeline cross-validation accuracy is hovering around 50% (random guessing). A previous data analyst mentioned there might be a silent data type conversion issue occurring when pandas reads the CSV files, likely introducing NaNs or coercing data types in a way that permanently destroys the signal in the `device_id` column before the model even sees it.

Your task:
1. Identify and fix the silent type coercion/precision bug in `/home/user/pipeline.py`. (Hint: Pay close attention to how large integers behave when missing values are present in pandas).
2. Ensure the pipeline uses cross-validation to evaluate the model. The fixed pipeline should easily achieve > 95% accuracy.
3. Run the fixed `/home/user/pipeline.py`. It is already configured to train on the full training set and output predictions for `test.csv` to `/home/user/predictions.csv`. 

Verify your success by ensuring `/home/user/predictions.csv` is generated and that the cross-validation score printed to the console is > 0.95. Do not change the model type or the random seed; only fix the data loading/preprocessing steps to prevent data corruption.