You are a data analyst setting up an automated pipeline to process text-based CSV data. You need to write a Python script for tokenization and cross-validated hyperparameter tuning, and a Bash script to configure the numerical libraries properly before execution to prevent thread oversubscription.

**Task Requirements:**

1. Create a Python script at `/home/user/train.py` that performs the following steps:
   - Verifies that the environment variables `OPENBLAS_NUM_THREADS` and `OMP_NUM_THREADS` are both explicitly set to `"1"`. If they are not, the script must exit with an error.
   - Loads the dataset from `/home/user/data.csv`. The CSV has two columns: `text` (string) and `target` (float).
   - Prepares the dataset by tokenizing the `text` column using `sklearn.feature_extraction.text.CountVectorizer` with `max_features=50` and `stop_words='english'`.
   - Performs hyperparameter tuning using `sklearn.model_selection.GridSearchCV` with a `Ridge` regressor (`random_state=42`). 
   - Tunes the `alpha` parameter over the grid `[0.1, 1.0, 10.0]`. Use 3-fold cross-validation (`cv=3`) and the default scoring metric (R^2).
   - Writes a JSON file to `/home/user/results.json` containing the best alpha and the mean cross-validated score for that alpha. Format the JSON exactly as follows:
     ```json
     {
       "best_alpha": <float>,
       "best_score": <float_rounded_to_4_decimal_places>
     }
     ```

2. Create a Bash script at `/home/user/run.sh` that:
   - Sets and exports the environment variables `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`.
   - Executes the `train.py` script.
   - Make sure `/home/user/run.sh` is executable.

The dataset `/home/user/data.csv` already exists in your environment.