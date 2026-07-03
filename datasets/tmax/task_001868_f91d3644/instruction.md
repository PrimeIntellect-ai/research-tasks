You are tasked with fixing and completing a Go-based data processing pipeline for a local data science experiment. The project directory is `/home/user/workspace`.

Currently, there is a Go program `pipeline.go` that reads a CSV file `/home/user/workspace/input.csv`. The pipeline has a silent data dropping bug: it drops rows where the `category_id` is empty instead of imputing them. 

Your tasks are:
1. **Fix the Data Bug**: Modify `pipeline.go` so that if the `category_id` field in the CSV is empty, it is silently imputed as `0` instead of failing to parse and skipping the row.
2. **Implement Embedding Computation**: Complete the `ComputeEmbedding(text string) []float64` function in `pipeline.go`. The mock embedding should be a float64 slice of length 3 containing:
   - Index 0: The total character length of the text.
   - Index 1: The number of vowels (a, e, i, o, u - case insensitive) in the text.
   - Index 2: The number of consonants (alphabetical characters that are not vowels) in the text.
3. **Evaluate and Track**: Complete the `Evaluate(records []Record) float64` function to return the average of the first embedding dimension (total character length) across all processed records. 
4. **Execution**: The main function should process `input.csv` and output a JSON file at `/home/user/workspace/metrics.json` containing the exact following structure:
```json
{
  "total_rows_processed": <int>,
  "evaluation_score": <float64>
}
```
5. Build and run your pipeline to generate the `metrics.json` file. 

Ensure the final Go code builds successfully by running `go build pipeline.go` and that running the compiled executable produces the correct JSON output.