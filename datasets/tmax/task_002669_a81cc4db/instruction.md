You are a data engineer tasked with debugging and testing a C++ ETL pipeline component. 

We have a C++ program in `/home/user/etl/aggregator.cpp` that reads a CSV file `/home/user/etl/data.csv`. The CSV contains two columns: `category` (string) and `value` (64-bit unsigned integer). Some `value` fields are missing (represented by an empty string). 
The current pipeline code reads the values, converts them to `double` to handle missing values (treating them as 0 for simplicity, though the previous developer used `std::stod` with a try-catch), and then casts them back to `uint64_t` to compute the sum per category.

However, this silent conversion through `double` causes precision loss for large 64-bit integers (values > 2^53). 

Your tasks are:
1. **Fix the Bug:** Modify `/home/user/etl/aggregator.cpp` so that it parses the values directly as `uint64_t` using `std::stoull` (ignoring empty strings, i.e., adding 0 for them) without losing precision.
2. **Compile and Run:** Compile the program to an executable `/home/user/etl/aggregator`. Run it on `/home/user/etl/data.csv`. The program should output the aggregated results to `/home/user/etl/results.csv` in the format `category,sum`.
3. **Reproducibility Test:** Create a C++ test file `/home/user/etl/test_aggregator.cpp` that tests the aggregation logic. It should compile to `/home/user/etl/run_tests` and exit with code 0 on success.
4. **Statistical Tracking:** Create a Python or C++ script that reads `/home/user/etl/results.csv`, calculates the exact mean and sample variance of the `sum` column (across all categories), and writes a report to `/home/user/etl/metrics.txt` exactly in this format:
```
Mean: <mean_value>
Variance: <variance_value>
```
(Round both values to 2 decimal places).

Ensure all requested files are created in the correct locations.