You are a Data Engineer building an automated ETL pipeline. Part of this pipeline involves running an inference performance benchmark on batches of processed data. 

You have been given a preliminary script located at `/home/user/etl_benchmark.py` that reads batch processing statistics from `/home/user/data/batch_stats.csv`. 

However, the script has several issues:
1. It is attempting to display a matplotlib plot interactively, which fails or produces a blank/corrupted plot in our headless Linux environment.
2. It fails to properly handle missing values (NaNs) and severe outliers in the `inference_time_ms` column. Specifically, any row with a missing `inference_time_ms` or an `inference_time_ms` strictly greater than `10000` must be completely removed from the dataset before any analysis or plotting occurs.
3. The script needs to compute the Pearson correlation and the covariance between `record_count` and `inference_time_ms` on the *cleaned* dataset, and save these precise metrics.

Your task:
1. Modify `/home/user/etl_benchmark.py` to fix the matplotlib backend issue so that it successfully saves a non-empty plot to `/home/user/benchmark_plot.png` (do not use `plt.show()`).
2. Implement the missing value and outlier filtering logic directly in the script as described above.
3. Ensure the script writes a JSON file to `/home/user/benchmark_results.json` containing exactly two keys: `"correlation"` and `"covariance"`. Both values must be calculated using `pandas` default methods (`corr()` and `cov()`) on the cleaned data, and rounded to exactly 4 decimal places.
4. Run the script to generate the output files.

Do not change the file paths. Ensure your final script executes successfully without errors.