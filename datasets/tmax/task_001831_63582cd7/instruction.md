You are an MLOps engineer tracking machine learning experiment artifacts. You have been given a set of experiment logs in JSON format located in `/home/user/experiments/`. 

Your objective is to write a Bash script at `/home/user/analyze_artifacts.sh` that processes these JSON files, cleans the data, and finds the most relevant experiment based on a target hyperparameter vector.

Your script must perform the following pipeline exclusively using Bash, standard command-line utilities (like `jq`, `awk`, `bc`), and basic shell scripting:

1. **Schema Enforcement & Missing Values**: Filter out any JSON files that do not perfectly match this schema:
   - `id`: string
   - `accuracy`: number
   - `loss`: number
   - `vector`: array of exactly 3 numbers
   If a file is missing any of these keys, or if the types/lengths do not match, ignore it.

2. **Outlier Handling**: From the schema-valid files, filter out any experiments where:
   - `accuracy` is less than 0.0 or strictly greater than 1.0.
   - `loss` is less than or equal to 0.0.

3. **Similarity Search**: For the remaining valid and clean experiments, calculate the squared Euclidean distance between their `vector` and the target ideal vector: `[1.0, 2.0, 3.0]`.

4. **Reporting**: Find the experiment with the **smallest** squared Euclidean distance to the target vector. Write ONLY its `id` string (without quotes) to `/home/user/closest.txt`.

Make sure your script is executable (`chmod +x /home/user/analyze_artifacts.sh`) and run it so that the output file `/home/user/closest.txt` is generated.