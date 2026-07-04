You are helping a data researcher fix and test a data processing pipeline. 

The researcher has a raw dataset of sensor measurements at `/home/user/data/raw_measurements.csv` and a Go program at `/home/user/pipeline/process.go` that is supposed to read this CSV, apply Min-Max normalization to the values, and output the results to `/home/user/data/processed.json`. 

However, they are experiencing an issue similar to "blank plots" in visualization tools: the pipeline runs without errors, but the output JSON contains entirely zeroes (`0.000`) for all normalized values.

Your task is to fix the pipeline, ensure its numerical accuracy, and make it reproducible:

1. **Fix the Bug**: Identify and fix the bug in `/home/user/pipeline/process.go`. The `Normalize` function should correctly apply Min-Max normalization: `(value - min) / (max - min)`. If all values are the same, it should return an array of `0.0`. Ensure the output values are accurate to at least 4 decimal places.

2. **Numerical Accuracy Testing**: Create a test file at `/home/user/pipeline/process_test.go`. 
   - Write a table-driven test for the `Normalize` function.
   - You must initialize a Go module named `data-pipeline` in the `/home/user/pipeline` directory.
   - Install and use the `github.com/stretchr/testify/assert` package to verify that the normalized values match expected outputs within a delta of `1e-4` (using `assert.InDeltaSlice` or similar).

3. **Pipeline Reproducibility**: Create a bash script at `/home/user/run_pipeline.sh` that, when executed:
   - Changes the current directory to `/home/user/pipeline`.
   - Downloads any necessary Go dependencies.
   - Runs the Go tests using `go test`.
   - If the tests pass, runs `process.go` to generate the final `/home/user/data/processed.json`.

The final JSON file must be an array of objects with the structure:
`[{"id": 1, "value": 0.41176}, ...]`

Ensure your `run_pipeline.sh` is executable (`chmod +x`).