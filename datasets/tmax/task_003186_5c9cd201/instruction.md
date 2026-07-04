You are acting as a machine learning engineer preparing a high-performance training data pipeline. We use a custom, fast C-based library called `fastagg` to perform tabular data transformation and aggregation (specifically computing moving averages and standard deviations on rolling windows) before feeding the data into our model.

The source code for this library is vendored at `/app/fastagg-1.0`. We recently upgraded our build system, but the `fastagg` package seems to have a bug that causes our numerical accuracy tests to fail. The standard deviation outputs are systematically off by a small amount, which degrades our model's downstream performance. 

Your tasks are to:
1. Identify and fix the numerical accuracy bug in `/app/fastagg-1.0/src/agg.c`. It is suspected that the calculation of the sample standard deviation is incorrect (e.g., using population standard deviation formula or missing Bessel's correction).
2. The `Makefile` in `/app/fastagg-1.0` is also slightly broken and fails to link the math library properly. Fix the Makefile so that running `make` inside `/app/fastagg-1.0` successfully builds the executable `/app/fastagg-1.0/fastagg`.
3. After building the tool, run it on our raw data file located at `/app/data/raw_features.csv`. You must output the results to `/home/user/processed_features.csv`.
The command usage is: `./fastagg <input_file> <output_file>`

Our automated verification will evaluate the numerical accuracy of your generated `/home/user/processed_features.csv` against our gold standard reference data, using Mean Squared Error (MSE) on the standard deviation columns.