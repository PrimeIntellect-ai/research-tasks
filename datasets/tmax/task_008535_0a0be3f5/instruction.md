I am an MLOps engineer maintaining a machine learning pipeline. We have a simple classification pipeline consisting of two scripts: `/home/user/preprocess.py` and `/home/user/train.py`. 

Recently, we added a new category to our raw data `/home/user/data_raw.csv`. Because of this, our preprocessing script is silently introducing `NaN` values during a feature mapping step, which causes pandas to automatically upcast the entire `group_id` column to `float64`. 

Our training script relies on `group_id` being strictly an integer for downstream processing and cross-validation, and it is currently crashing with a `TypeError`.

Your task is to:
1. Identify and fix the bug in `/home/user/preprocess.py`. You must handle the unmapped category values by filling missing values in the `group_id` column with `-1`, and ensure the column is correctly cast to the `int64` data type.
2. Run `python3 /home/user/preprocess.py` to generate the intermediate data artifact.
3. Run `python3 /home/user/train.py` to perform cross-validation and generate the final evaluation artifact at `/home/user/best_score.txt`.

Do not modify `/home/user/train.py` or `/home/user/data_raw.csv`. Only fix the preprocessing script and successfully run both scripts to produce the score file.