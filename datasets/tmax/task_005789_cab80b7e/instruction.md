You are an ML engineer tasked with migrating our data preprocessing and sampling pipeline to Go so it can be shared with our low-latency production systems. 

You have been provided a raw dataset at `/home/user/raw_metrics.csv` containing server performance logs. The CSV has the following columns: `ID`, `CPU`, `Memory`, `DiskIO`, and `Latency`.

Your task is to write and execute a Go program (`/home/user/pipeline.go`) that does the following:

1. **Feature Engineering**: 
   - Parse the CSV.
   - Create a new feature called `LoadIndex`, calculated as `(CPU * Memory) / DiskIO`.
   
2. **Tabular Transformation**:
   - Perform Min-Max scaling on `CPU`, `Memory`, `DiskIO`, and `LoadIndex`. 
   - The formula for Min-Max scaling is `(x - min) / (max - min)`. Calculate the minimum and maximum for each column based on the entire dataset.
   - Save this transformed dataset (including the unscaled `ID` and `Latency`) to `/home/user/processed_metrics.csv`. The columns must be in this exact order: `ID, CPU_scaled, Memory_scaled, DiskIO_scaled, LoadIndex_scaled, Latency`. All float values should be formatted to 4 decimal places.

3. **Bootstrap Sampling**:
   - We need to estimate the confidence interval of the mean Latency using bootstrapping.
   - Initialize a Go random number generator using `rand.New(rand.NewSource(12345))`. 
   - Generate exactly 5 bootstrap samples from the *transformed* dataset. A bootstrap sample is created by randomly sampling rows with replacement until you have a dataset of the same size as the original dataset (N rows).
   - *Important Note on Randomness*: To ensure deterministic output, generate the random row indices for each sample sequentially. For each row in a bootstrap sample, pick an index using `rng.Intn(N)`. Do this N times for the first sample, then N times for the second, etc. Use 0-based indexing relative to the data rows.
   - For each of the 5 bootstrap samples, calculate the mean of the `Latency` column.

4. **Reporting**:
   - Write the array of the 5 bootstrap mean latencies to a JSON file at `/home/user/bootstrap_means.json`. 
   - The JSON should be a simple array of 5 floats: `[mean1, mean2, mean3, mean4, mean5]`.

Ensure your program compiles and runs successfully, producing both `/home/user/processed_metrics.csv` and `/home/user/bootstrap_means.json`.