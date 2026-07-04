You are an engineer managing a multi-language configuration system. We track changes to localized configuration descriptions over time, but the data is currently in a wide format and needs to be analyzed for translation divergence.

You need to write a Go program at `/home/user/analyze.go` that processes an input CSV and produces an aggregated summary.

**Input Data:**
There is a CSV file located at `/home/user/data/config_commits.csv` (which will be created before you start). It has no header. The columns are:
1. `timestamp`: Unix epoch time in seconds.
2. `config_key`: A string identifier for the configuration.
3. `val_en`: The English description.
4. `val_ru`: The Russian description.
5. `val_ja`: The Japanese description.

**Requirements for `/home/user/analyze.go`:**
1. **Time-based Bucketing**: Convert the `timestamp` into UTC hourly buckets formatted as `YYYY-MM-DDTHH` (e.g., `2023-10-25T14`).
2. **Wide-long Reshaping**: For each row, extract two language pairs to compare: `en-ru` (comparing `val_en` to `val_ru`) and `en-ja` (comparing `val_en` to `val_ja`).
3. **Distance Computation**: Implement a custom, Unicode-aware Levenshtein distance function in Go. **Important:** The distance must be calculated over Unicode characters (runes), not raw bytes! 
4. **Aggregation**: For each unique combination of `bucket`, `config_key`, and `lang_pair`, find the **maximum** Levenshtein distance observed in that hour.
5. **Output**: Write the aggregated results to `/home/user/output.csv` with the following columns (include this exact header row):
   `bucket,config_key,lang_pair,max_distance`
   Sort the output CSV first by `bucket` (ascending), then by `config_key` (ascending), and finally by `lang_pair` (ascending).

**Constraints:**
* Use only the standard Go library (no external packages like `github.com/...`).
* Ensure your Go program compiles and can be executed via `go run /home/user/analyze.go`.
* Ensure you handle UTF-8 strings correctly (e.g. "ログイン" is 4 runes).

Once you have written the code, run it to generate `/home/user/output.csv`.