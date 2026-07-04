You are an ML Engineer preparing training data and validating previous model outputs for a new Bayesian inference pipeline. 

We have a set of raw JSON files stored in `/home/user/raw_data/` simulating a partitioned data lake. Each JSON file contains an array of objects representing prior predictions and new evidence likelihoods. The structure of each object is:
`{"id": int, "prior": float, "likelihood": float, "actual_class": int}`

Your task is to write a Go program `/home/user/etl_pipeline.go` that acts as an ETL (Extract, Transform, Load) script to process this data. The program should do the following:

1. **Extract**: Read all `.json` files in the `/home/user/raw_data/` directory.
2. **Validate**: Check each record. A record is ONLY valid if:
   - `prior` is between 0.0 and 1.0 (inclusive).
   - `likelihood` is between 0.0 and 1.0 (inclusive).
   - `actual_class` is exactly `0` or `1`.
3. **Transform (Bayesian Math)**: For all *valid* records, calculate the joint probability of the actual class occurring.
   - If `actual_class == 1`: `joint_prob = prior * likelihood`
   - If `actual_class == 0`: `joint_prob = (1.0 - prior) * (1.0 - likelihood)`
4. **Load/Summarize**: The program must output a single summary JSON file to `/home/user/summary.json` containing the exact following structure:
   ```json
   {
     "valid_count": <integer>,
     "invalid_count": <integer>,
     "average_joint_prob": <float>
   }
   ```
   *Note: `average_joint_prob` is the mean of the `joint_prob` across all VALID records only.*

To complete this task:
1. Initialize a Go module (e.g., `go mod init etl`) in `/home/user/`.
2. Write the Go code in `/home/user/etl_pipeline.go`.
3. Compile and run the code to produce `/home/user/summary.json`.

Please implement this and ensure `/home/user/summary.json` is correctly generated.