I need your help cleaning and preparing a time-series dataset of sensor readings for downstream machine learning. I was provided with a custom Python package for our data processing pipeline, but it seems to have a bug and isn't working correctly.

Here is what you need to do:
1. There is a vendored package located at `/app/ts_processor/`. This package is supposed to provide a function `process_and_validate(df, freq)` that takes a pandas DataFrame, removes duplicates, resamples it to the given frequency, interpolates missing values linearly, and validates constraints (e.g., all values must be between 0 and 100). However, the package contains a bug in its gap-filling logic that causes it to crash or produce incorrect results when resampling.
2. Fix the bug in `/app/ts_processor/ts_processor/core.py`.
3. Install the package locally.
4. Write a Python script `/home/user/clean_data.py` that reads a raw, messy dataset from `/home/user/raw_sensor_data.csv`.
5. The raw dataset has columns `timestamp` and `value`. It contains duplicate timestamps, out-of-bounds noise (values < 0 or > 100), and missing intervals. Before using the package, you must filter out any rows where `value` is less than 0 or greater than 100 to clean the noise.
6. Use the `process_and_validate` function from the fixed `ts_processor` package to resample the filtered data to a daily frequency (`'D'`) and fill the gaps.
7. Save the resulting processed DataFrame to `/home/user/processed_sensor_data.csv`.

Your final output file must be a CSV containing exactly two columns: `timestamp` and `value`. The automated system will evaluate the accuracy of your gap-filling interpolation against a hidden ground-truth dataset.