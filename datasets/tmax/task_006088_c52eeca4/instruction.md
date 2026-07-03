You are an MLOps engineer tasked with analyzing experiment artifacts. In the directory `/home/user/artifacts`, you will find several JSON files, each representing an experiment's metadata and performance metrics. 

Your objective is to:
1. **Enforce Data Schema**: Filter the JSON files based on the following valid schema:
   - Must contain a key `"experiment_id"` (string).
   - Must contain a key `"status"` with the exact value `"SUCCESS"`.
   - Must contain a key `"metrics"`, which is an array of exactly 5 numbers.
   Any file that does not strictly adhere to this schema should be ignored.

2. **Similarity Search via Linear Algebra**: For the valid experiments, treat their `"metrics"` arrays as 5-dimensional numerical vectors. Calculate the pairwise cosine similarity between all valid experiments.

3. **Reporting**: Identify the single pair of distinct valid experiments that have the highest cosine similarity.
   Create a JSON file at `/home/user/most_similar.json` containing the result in exactly this format:
   ```json
   {
     "exp1": "<experiment_id_1>",
     "exp2": "<experiment_id_2>",
     "similarity": <similarity_score>
   }
   ```
   *Constraints for the output*:
   - `<experiment_id_1>` must be lexicographically smaller than `<experiment_id_2>` (e.g., "exp_a" comes before "exp_b").
   - `<similarity_score>` must be the cosine similarity rounded to exactly 4 decimal places (e.g., 0.9990).

You may use any programming language (e.g., Python, Bash + jq) to accomplish this task. Ensure your final output is precisely at `/home/user/most_similar.json` with the specified format.