You are an AI assistant helping a data scientist clean a multilingual dataset.

You have been given a user metadata file and several partitioned files containing product reviews in different languages. The review texts contain unnormalized Unicode (e.g., NFD instead of NFC) and need to be joined with the metadata. 

Your task is to write a Go program at `/home/user/workspace/clean_data.go` that does the following:
1. Loads the metadata from `/home/user/workspace/metadata.csv`.
2. Concurrently reads all CSV files matching the pattern `/home/user/workspace/reviews_*.csv`. You must use Goroutines to process the review files in parallel.
3. Performs an inner join between the metadata and the reviews based on the `user_id` column.
4. Normalizes the `review_text` for each row to Unicode NFC (Normalization Form C).
5. Outputs the joined, normalized data to `/home/user/workspace/output.jsonl` in JSON Lines format.

### File Schemas
**metadata.csv:**
```csv
user_id,username,country
```

**reviews_*.csv:**
```csv
user_id,review_text
```

### Output Format
The file `/home/user/workspace/output.jsonl` must contain one JSON object per line. Keys must be strictly:
- `user_id` (string)
- `username` (string)
- `country` (string)
- `normalized_review` (string)

The output does not need to be sorted.

### Environment constraints:
- Work within `/home/user/workspace`. 
- The directory is already a Go module (`go mod init data-clean`).
- You may install external modules if needed (e.g., `golang.org/x/text/unicode/norm`).
- Run your Go program to generate the final `output.jsonl` file.