You are a machine learning engineer tasked with preparing a training dataset and deploying a simple model serving API. 

We have vendored a custom internal Python package called `text_prep_serve` at `/app/text_prep_serve`. This package is supposed to:
1. Join two data sources (`data/texts.csv` and `data/labels.csv`) on the `id` column.
2. Tokenize the text and extract features using TF-IDF.
3. Split the data into train and test sets (80/20 split, without shuffling for this specific time-series data).
4. Apply bootstrap sampling to create 3 training subsets from the train split.
5. Train an ensemble of 3 Logistic Regression models (one on each bootstrap sample).
6. Serve the ensemble via a FastAPI HTTP server on port 8000.

However, the package is currently broken:
1. **Broken Package**: The `Makefile` in `/app/text_prep_serve` has a typo in the `install` target that prevents installation. Fix the `Makefile` and install the package dependencies.
2. **Data Leak**: The preprocessing script `src/prepare.py` has a critical data leakage bug. It fits the TF-IDF vectorizer on the *entire* dataset (train + test) before splitting, which artificially inflates the vocabulary and test performance. You must modify `src/prepare.py` so that the vectorizer is **only fitted on the training split**, and then transforms both train and test splits. The split logic itself (first 80% train, last 20% test) must remain exactly the same.
3. **Execution**: Run the dataset preparation to generate the models and vocabulary.
4. **Serving**: Start the API server on `127.0.0.1:8000`.

To complete the task:
1. Fix the `Makefile` in `/app/text_prep_serve`.
2. Fix the data leak in `/app/text_prep_serve/src/prepare.py`.
3. Generate the prepared models by running the preparation step (e.g., `python src/prepare.py`). The models and vectorizer should be saved to `/app/text_prep_serve/models/`.
4. Start the server as a background process using `python src/server.py`. The server must listen on `127.0.0.1:8000` and expose a POST endpoint at `/predict` accepting JSON like `{"text": "example document"}` and returning `{"prediction": 1}` (an integer representing the majority vote of the ensemble).

Leave the server running. We will verify your fix by sending HTTP POST requests to your server and checking the API responses, which will only match our expected outputs if the data leak was properly fixed and the bootstrap ensemble was trained correctly.