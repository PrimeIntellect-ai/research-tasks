You are managing an automated configuration tracking system. Configuration snapshots of a server are periodically saved in the directory `/home/user/configs/`. The snapshots are named following the pattern `config_YYYY-MM-DDTHH.txt`. 

However, the snapshot service occasionally fails, leaving gaps in the hourly sequence. Your task is to write and execute a Python script `/home/user/analyze_configs.py` that processes these configurations, fills the gaps, normalizes the data, and computes the change similarity between consecutive hours.

Here are the specific requirements for your script:

1. **Resampling and Gap-filling**:
   - Determine the earliest and latest hourly timestamps present in the `/home/user/configs/` directory.
   - Generate a complete hourly sequence from the earliest to the latest timestamp (inclusive).
   - If an hourly snapshot is missing, apply "forward filling" by copying the contents of the most recent available preceding hour's snapshot. 

2. **Tokenization and Normalization**:
   - For each hour's configuration, read the file line by line.
   - Normalize each line by stripping leading and trailing whitespace and converting all characters to lowercase.
   - Ignore empty lines and lines that begin with a `#` character (comments) after stripping.
   - Treat the remaining normalized lines as an unordered set of unique configuration tokens for that hour.

3. **Similarity Computation**:
   - Calculate the Jaccard similarity between the configuration sets of each consecutive hourly pair (Hour $H$ and Hour $H+1$).
   - The Jaccard similarity of two sets $A$ and $B$ is the size of their intersection divided by the size of their union. If both sets are empty, the similarity is `1.0`.

4. **Output**:
   - Generate a CSV file at `/home/user/similarity_report.csv`.
   - The CSV must have exactly this header: `timestamp1,timestamp2,jaccard_similarity`
   - `timestamp1` and `timestamp2` are the consecutive hourly timestamps (e.g., `2023-10-01T00`).
   - `jaccard_similarity` must be formatted to exactly 4 decimal places (e.g., `0.2000`).

Ensure your script is self-contained, handles the file reading properly, and outputs the exact CSV format requested. Execute your script so the CSV is created.