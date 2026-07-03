You are a localization engineer managing subtitle translation pipelines. A recent automated export of localized subtitle time-series data was corrupted. The timing data has gaps, and the text contains malformed localization tags. 

Your objective is to build a Go-based data pipeline to stream, repair, normalize, and export this data into a SQLite database, achieving a high Localization Quality Score (LQS) as graded by our proprietary black-box evaluator.

**Input Data:**
The raw data is located at `/home/user/raw_subs.csv`. It is a large CSV file with the following headers: `id,start_ms,end_ms,raw_text`.
- The file is large; your Go program must stream the data rather than loading it entirely into memory.
- `id` is a sequential integer.
- `start_ms` and `end_ms` are time-series timestamps in milliseconds. Many entries have `-1` for these fields, indicating missing data. 

**Requirements:**

1. **Interpolation & Imputation:**
   Write a Go program at `/home/user/pipeline.go` that streams the CSV. When it encounters missing timestamps (`-1`), it must linearly interpolate the `start_ms` and `end_ms` values based on the nearest valid preceding and succeeding rows. Round the interpolated milliseconds to the nearest integer.

2. **Tokenization & Normalization:**
   For the `raw_text` field:
   - Remove all pseudo-HTML tags (e.g., `<i>`, `</font>`, `<c.color>`).
   - Remove all punctuation characters.
   - Convert all text to lowercase.
   - Collapse multiple spaces into a single space, stripping leading/trailing whitespace.

3. **Output & Database Export:**
   - The Go program should stream its output to a cleaned CSV at `/home/user/clean_subs.csv`.
   - Bulk import this cleaned CSV into a SQLite database at `/home/user/subs.db`. The table must be named `subtitles` with the schema: `(id INTEGER PRIMARY KEY, start_ms INTEGER, end_ms INTEGER, text TEXT)`.

4. **Evaluation:**
   We have provided a stripped, compiled binary at `/app/eval_lqs` that calculates the Localization Quality Score based on temporal consistency, imputation accuracy, and token normalization. 
   - Usage: `/app/eval_lqs /home/user/subs.db`
   - It outputs a single numerical score between 0.0 and 1.0.

**Success Criteria:**
Your final pipeline must execute successfully, correctly populate `/home/user/subs.db`, and when evaluated by `/app/eval_lqs`, achieve a score of **0.95 or higher**. Save the console output of the evaluator to `/home/user/final_score.txt`.