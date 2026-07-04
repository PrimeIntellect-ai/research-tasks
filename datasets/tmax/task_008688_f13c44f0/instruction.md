You are a researcher organizing and benchmarking a simple inference pipeline. You have two datasets:
- `/home/user/data/features.csv`: Contains input features (header: `id,x,y,z`).
- `/home/user/data/labels.csv`: Contains ground truth labels (header: `id,label`).

Your task is to build a fast C-based inference program and a reproducible shell pipeline to evaluate it.

Step 1: Write a C program `/home/user/src/model.c`.
The program should:
- Take the path to `features.csv` as its first command-line argument.
- Read the CSV file (ignoring the header).
- For each row, calculate a score using the formula: `score = x*0.5 + y*0.3 + z*0.2`.
- Make a prediction: if `score > 0.5`, the prediction is `1`, otherwise `0`.
- Output the results to standard output in CSV format: `id,prediction` (include the header `id,prediction` as the first line).

Step 2: Write a shell script `/home/user/pipeline.sh`.
The script must:
- Compile `/home/user/src/model.c` into an executable at `/home/user/src/model` using `gcc` with `-O3` optimization.
- Execute the compiled `model` on `/home/user/data/features.csv` and capture the output.
- Join the prediction output with `/home/user/data/labels.csv` based on the `id` column.
- Calculate the accuracy of the predictions (percentage of matching labels).
- Write the final accuracy to `/home/user/accuracy.txt` in exactly this format: `Accuracy: XX.XX%` (where XX.XX is the percentage rounded to two decimal places).

Ensure your script is executable (`chmod +x /home/user/pipeline.sh`) and runs successfully. You may use standard Unix text processing tools (like `awk`, `join`, `sed`) or install user-local Python packages if you choose to do the joining in Python.