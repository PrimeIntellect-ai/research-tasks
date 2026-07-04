You are helping a data science researcher organize and operationalize a messy dataset of research paper abstracts. 

We are using a custom internal data processing package called `textprep_lib`. Its source is vendored in your environment at `/app/textprep_lib-0.4.5`. However, there is a bug in how it cleans metadata: when handling missing values (represented as the string `'None'`) in the integer `citations` column, it inadvertently introduces standard `NaN`s, which silently converts the entire column to floats. This loss of schema fidelity breaks our strict numerical accuracy and schema enforcement checks downstream.

Your objectives are:

1. **Fix the Package**: Inspect and modify `/app/textprep_lib-0.4.5/textprep_lib/preprocess.py` to fix this bug. The missing `'None'` values in the `citations` column should be replaced with `0`, and the column must be strictly cast to standard `int` (or `int64`). Install the package locally in editable mode.
2. **Process and Evaluate**: 
   - Load the dataset located at `/home/user/data/abstracts.csv` using the fixed `textprep_lib.preprocess.load_and_clean` function.
   - Vectorize the `abstract` column using standard TF-IDF (scikit-learn, `max_features=100`, English stop words).
   - Combine the TF-IDF features with the `citations` column.
   - Perform 5-fold cross-validation using a standard `LogisticRegression` to predict the binary `is_accepted` column. 
   - Save the mean accuracy of the cross-validation to a file at `/home/user/cv_result.txt` (just the number as a float).
3. **Train and Serve**: 
   - Train the `LogisticRegression` pipeline on the entire dataset.
   - Bring up a Python web service (e.g., Flask or FastAPI) listening on exactly `127.0.0.1:5000`.
   - Expose a `POST` endpoint at `/predict`.
   - The endpoint must require a bearer token for authorization. The expected token is `ds-research-token-881` (passed as `Authorization: Bearer ds-research-token-881`).
   - The endpoint should accept a JSON payload: `{"abstract": "<text>", "citations": <int>}`.
   - It must return a JSON response: `{"prediction": <int>}` where `<int>` is the predicted class (0 or 1).

Please begin. Leave the service running in the background or foreground so it can be tested.