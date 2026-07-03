You are a machine learning engineer tasked with building an ETL pipeline to prepare text data, testing its reproducibility, and benchmarking its inference performance.

Your environment has `scikit-learn`, `numpy`, `pandas`, and `joblib` installed.
A raw dataset is located at `/home/user/data/raw.jsonl`. Each line is a JSON object with a `"text"` field.

Please complete the following tasks:

1. **ETL Pipeline Construction**
   Write a Python script `/home/user/etl.py` that does the following:
   - Reads all lines from `/home/user/data/raw.jsonl`.
   - Extracts the `"text"` field from each JSON object.
   - Preprocesses the text by converting it to lowercase and stripping leading/trailing whitespace.
   - Fits a `TfidfVectorizer` from `scikit-learn` with `max_features=100` and `stop_words='english'`.
   - Fits a `TruncatedSVD` on the TF-IDF output with `n_components=10` and `random_state=42`.
   - Saves the transformed numerical features as a NumPy array to `/home/user/data/features.npy`.
   - Saves the fitted vectorizer to `/home/user/models/vectorizer.joblib` and the SVD model to `/home/user/models/svd.joblib`. 
   (Create the `/home/user/models/` directory if it does not exist).
   Run this script to generate the artifacts.

2. **Pipeline Reproducibility Testing**
   Write a script `/home/user/reproducibility_test.py` that:
   - Programmatically executes the ETL process described above twice.
   - Compares the resulting feature matrices.
   - If the NumPy arrays are exactly equal (use `numpy.array_equal`), write the string `"PASS"` to `/home/user/test_result.txt`. Otherwise, write `"FAIL"`.
   Run this script so that `/home/user/test_result.txt` is created.

3. **Inference Performance Benchmarking**
   Write a script `/home/user/benchmark.py` that:
   - Loads the saved vectorizer and SVD models from `/home/user/models/`.
   - Loads the text data from `/home/user/data/raw.jsonl` and applies the lowercase/strip preprocessing.
   - Measures the total time it takes to transform (NOT fit) the entire dataset through both the vectorizer and the SVD model.
   - Repeats this transformation process for 50 iterations.
   - Calculates the average time per iteration in seconds.
   - Saves the results to `/home/user/metrics.json` in the following exact format:
     ```json
     {
       "num_runs": 50,
       "avg_time_seconds": <float>
     }
     ```
   Run this script to generate `/home/user/metrics.json`.