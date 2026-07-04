You are a data engineer tasked with building a lightweight ETL pipeline in Go that extracts text data, engineers features via dimensionality reduction (the Hashing Trick), and tracks experiment metrics.

Your objective is to write and execute a Go program at `/home/user/etl.go` that processes customer feedback and generates numerical embeddings.

**Input Data:**
A CSV file is located at `/home/user/data/feedback.csv` with the headers: `id,timestamp,text,rating`.

**Requirements for `/home/user/etl.go`:**
1. **Read the CSV:** Parse `/home/user/data/feedback.csv`.
2. **Feature Engineering & Tokenization:** For each `text` field:
   - Convert the entire string to lowercase.
   - Remove all occurrences of the following punctuation characters: `.`, `,`, `!`, `?`
   - Split the cleaned string into tokens using standard whitespace (e.g., `strings.Fields` in Go).
3. **Dimensionality Reduction (Hashing Trick):** Map the variable-length tokens into a fixed-size integer array of length 10.
   - Initialize an array of 10 integers (all zeros) for the row.
   - For each token, compute its 32-bit FNV-1a hash (using Go's standard `hash/fnv` package).
   - Compute the index as: `hash_value % 10`.
   - Increment the value at that index in the array by 1.
4. **Export Embeddings:** Write the results to `/home/user/output/embeddings.jsonl`.
   - Each line must be a JSON object with two keys: `"id"` (string) and `"vector"` (array of 10 integers).
   - Order the lines exactly as they appear in the input CSV (skipping the header).
5. **Experiment Tracking:** Append a summary line to `/home/user/output/run_metrics.txt` in the exact format: `Run completed. Total records processed: <N>` (where `<N>` is the number of data rows processed, excluding the header).

**Constraints:**
- Use only standard Go library packages.
- Ensure the output directory `/home/user/output/` exists or is created by your program.
- Do not include the header row in your JSONL output.

Write the code, compile/run it, and ensure the output files are generated precisely as specified.