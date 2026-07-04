You are a data scientist tasked with cleaning and analyzing server performance metrics. The raw data is messy, contains missing values, and has outliers. You need to write a Go program to process this dataset, perform feature aggregation, and find similar servers.

Write a Go program (e.g., at `/home/user/workspace/process.go`) that performs the following steps:

1. **Read Data**: Read a CSV file located at `/home/user/data/servers.csv`.
   - Columns: `ServerID`, `CPU`, `Mem`, `Disk`, `NetIn`, `NetOut`
   - All columns except `ServerID` are floating-point numbers.
   - Some fields are empty strings (missing values).

2. **Missing Value Imputation**:
   - For each numeric column (`CPU`, `Mem`, `Disk`, `NetIn`, `NetOut`), compute the mean of the available (non-empty) values.
   - Replace any missing (empty) values with the corresponding column's mean.

3. **Outlier Handling**:
   - After imputation, filter out any rows where `CPU > 100.0` or `Mem > 100.0`. These are considered invalid outlier records.

4. **Dimensionality Reduction / Aggregation**:
   - Drop the `Disk` column entirely.
   - Create a new feature `NetTotal` which is the sum of `NetIn` and `NetOut`.

5. **Similarity Search**:
   - We want to find servers similar to `ServerID` "S-10".
   - Represent each server as a feature vector: `[CPU, Mem, NetTotal]`.
   - Compute the Euclidean distance between "S-10" and all other valid servers.
   - Identify the top 2 most similar servers to "S-10" (i.e., the 2 servers with the lowest Euclidean distance, excluding "S-10" itself). If there is a tie, sort alphabetically by `ServerID`.

6. **Output**:
   - Write the cleaned tabular data to `/home/user/output/cleaned.csv` with columns: `ServerID,CPU,Mem,NetTotal`. Format all floating-point numbers to exactly 2 decimal places.
   - Write the `ServerID`s of the top 2 most similar servers to `/home/user/output/similar.txt`, one per line, ordered from most similar to least similar.

Setup instructions:
- Use standard Go libraries (e.g., `encoding/csv`, `math`, `strconv`).
- You must create the `workspace` and `output` directories if they do not exist.
- Run your Go program to generate the required outputs.