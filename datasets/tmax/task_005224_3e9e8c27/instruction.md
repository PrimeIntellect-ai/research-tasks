You are an MLOps engineer tasked with reconstructing a legacy experiment tracking pipeline. The previous engineer left behind some raw datasets and model weights, but the inference pipeline is missing. 

You need to recreate the pipeline by writing a data joining script and a C++ inference engine.

You are provided with the following files:
1. `/home/user/data/features.csv`: Contains model features.
2. `/home/user/data/metadata.csv`: Contains run metadata.
3. `/home/user/models/v2_weights.txt`: Contains a single line of comma-separated weights `w1,w2,w3,b` for the "v2" model.

Your task:
1. Write a C++ program at `/home/user/infer.cpp` that:
   - Takes the path to the weights file as its first command-line argument.
   - Reads the weights `w1,w2,w3,b`.
   - Reads comma-separated rows from `stdin` in the exact format: `id,f1,f2,f3,timestamp,model_version`.
   - For each row, computes the output using a linear layer followed by a ReLU activation function: `prediction = max(0.0, w1*f1 + w2*f2 + w3*f3 + b)`.
   - Prints the result to `stdout` in the format `id,prediction`, where the prediction is formatted to exactly 4 decimal places.

2. Write a bash script at `/home/user/run_pipeline.sh` that:
   - Compiles `/home/user/infer.cpp` to an executable named `/home/user/infer` using `g++` (assume C++17 standard).
   - Properly joins `/home/user/data/features.csv` and `/home/user/data/metadata.csv` on the `id` column.
   - Filters the joined data to keep ONLY the rows where `model_version` is exactly `v2`.
   - Strips any headers and passes the filtered, joined rows via `stdin` to the compiled `./infer` program.
   - Redirects the C++ program's output to `/home/user/predictions.csv`.
   - Calculates the average of all predictions in `/home/user/predictions.csv` and saves it to `/home/user/summary.txt`, formatted to exactly 4 decimal places (e.g., `0.1234`).

Constraints:
- Use standard bash commands (`join`, `awk`, `sort`, `grep`, etc.) for data manipulation in your script.
- Ensure your script exits with code 0 on success.
- Ensure the pipeline can be run simply by executing `bash /home/user/run_pipeline.sh`.