You are a data engineer tasked with fixing and extending an ETL pipeline, then serving its results via an HTTP API.

You have been provided with the following files:
1. `/app/audio/sample.wav`: An audio file.
2. `/home/user/data/primary.csv`: Contains columns `id` (integer), `text_description` (string), and `feature_val` (float).
3. `/home/user/data/secondary.csv`: Contains columns `id` (integer) and `category` (string). Note: This file has a missing `category` for one row, which introduces a NaN.
4. `/home/user/etl.py`: A buggy pandas pipeline script that joins these two CSVs. Currently, due to how pandas handles NaNs during merges, the `id` column silently converts from integers to floats.

Your tasks:
1. **Fix the ETL bug**: Modify `/home/user/etl.py` (or write your own script) to join `primary.csv` and `secondary.csv` on `id` using a left join. Ensure the `id` column strictly remains an integer (e.g., using pandas' `Int64` dtype or filling/dropping NaNs appropriately so the type is preserved).
2. **Audio Feature Extraction**: Load `/app/audio/sample.wav` using `librosa` at its native sampling rate. Extract 13 MFCCs (`librosa.feature.mfcc(..., n_mfcc=13)`) and compute the mean of each coefficient across the time axis, resulting in a 13-dimensional vector.
3. **Data Preparation & Tokenization**: For each row in the joined data, tokenize the `text_description` by splitting on whitespace, and compute the `token_count`. Create a combined feature vector for each row containing the `feature_val` and the 13 audio MFCC means (so each row has a 14-dimensional vector, where the audio features are identical across all rows).
4. **Dimensionality Reduction**: Fit a scikit-learn PCA model on these 14-dimensional vectors across the entire dataset to reduce them to 2 dimensions (`pca_1`, `pca_2`).
5. **API Serving & Benchmarking**: Create and start a Python web server (e.g., using Flask or FastAPI) listening on exactly `127.0.0.1:8000`. It must implement two GET endpoints:
   - `/record?id=<int>`: Should return a JSON response: `{"id": <integer>, "token_count": <integer>, "pca_1": <float>, "pca_2": <float>}`. The `id` must be a pure integer in the JSON, not a float, proving you fixed the pandas bug.
   - `/benchmark`: Should execute the PCA `.transform()` step 1000 times sequentially on the dataset, measure the total time taken, and return: `{"avg_inference_time_ms": <float>}` (the average time per transform call in milliseconds).

Keep the server running in the background so it can be tested.