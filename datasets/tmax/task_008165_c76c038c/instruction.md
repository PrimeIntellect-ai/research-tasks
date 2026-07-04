As an MLOps engineer, you need to write a C++ utility to track and validate experiment artifacts. In `/home/user/experiments/`, you will find a metadata file `metadata.csv` and a directory of embedding vectors `/home/user/experiments/embeddings/`.

The `metadata.csv` file has the following format:
```csv
model_id,epoch,embedding_file
model_A,10,emb_A.txt
model_B,10,emb_B.txt
...
```

The embedding files are simple text files containing space-separated floating-point numbers representing a vector.

Your task is to write and execute a C++ program at `/home/user/validate_artifacts.cpp` that performs the following:
1. Multi-source join: Reads `metadata.csv` and the corresponding embedding file for each row.
2. Model output validation: Checks if the embedding is valid. An embedding is valid if and only if it has exactly 5 dimensions (exactly 5 numeric values) and contains no `NaN` or `Inf` values.
3. Embedding computation: For valid embeddings, compute the Euclidean distance to a target reference embedding vector consisting of five ones: `[1.0, 1.0, 1.0, 1.0, 1.0]`.
4. Writes the results to `/home/user/experiments/validation_report.csv` with a header `model_id,is_valid,distance`.
   - `is_valid` should be `1` if valid, `0` if invalid.
   - `distance` should be formatted to exactly 4 decimal places (e.g., `0.0000`, `2.2361`).
   - If the embedding is invalid, output `-1.0000` for the distance.

Compile your code using `g++ -std=c++17 /home/user/validate_artifacts.cpp -o /home/user/validate_artifacts` and execute it to generate the report. Do not use any external libraries other than the standard C++ library.