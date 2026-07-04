You are an AI assistant acting as a Data Engineer/Data Scientist. Your task is to build a reproducible ETL and statistical analysis pipeline in Go. 

We have a raw dataset of sensor readings located at `/home/user/sensor_data.csv`. The CSV has a header row and four columns: `timestamp`, `sensor_A`, `sensor_B`, `sensor_C`.

Your objective is to write a Go program that processes this data, computes specific statistical metrics, and validates the results based on predefined rules. Furthermore, you must wrap this in a reproducible pipeline using a `Makefile`.

Here are the exact requirements:

1. **ETL / Data Cleaning Phase:**
   - Read the CSV file `/home/user/sensor_data.csv`.
   - Filter out any rows that contain invalid data. A row is considered invalid and must be dropped if:
     - Any of the sensor values (`sensor_A`, `sensor_B`, `sensor_C`) cannot be parsed as a float.
     - Any of the sensor values are less than `0.0`.
     - Any of the sensor values are greater than `1000.0`.
   - The `timestamp` column can be ignored for the statistical calculations but you must correctly handle the CSV structure.

2. **Statistical Analysis Phase:**
   - Using the cleaned data, compute the **Sample Pearson Correlation Coefficient** between `sensor_A` and `sensor_B`.
   - Compute the **Sample Covariance** between `sensor_A` and `sensor_C`.
   - Note: Use the standard formula for *sample* statistics (i.e., dividing by `N-1` where N is the number of valid rows).

3. **Model Validation Phase:**
   - We have a validation rule for this sensor cluster: The correlation between A and B must be strongly positive.
   - If the computed correlation between `sensor_A` and `sensor_B` is `>= 0.8000`, the validation status is `"pass"`. Otherwise, it is `"fail"`.

4. **Output Generation:**
   - The Go program must output the results to `/home/user/output/metrics.json`. (Create the `output` directory if it does not exist).
   - The JSON file must strictly follow this structure:
     ```json
     {
       "correlation_A_B": 0.1234,
       "covariance_A_C": 12.3456,
       "validation_status": "pass"
     }
     ```
   - Both float values must be rounded to exactly **4 decimal places**.

5. **Reproducible Pipeline Construction:**
   - Write all your Go code in `/home/user/pipeline.go`. You may use standard Go libraries (no third-party statistical packages allowed).
   - Create a `Makefile` at `/home/user/Makefile`.
   - The `Makefile` must contain a `run` target. When `make run` is executed in the terminal, it should compile the Go code and run the pipeline, successfully generating the `/home/user/output/metrics.json` file.

Ensure your code is robust and handles the required logic precisely.