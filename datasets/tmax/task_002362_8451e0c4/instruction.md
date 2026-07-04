You are a performance engineer analyzing the scaling and variance of different application components. You have collected a log of execution times in `/home/user/perf_logs.csv`. The CSV has three columns: `Function` (the component name), `DataSize` (the size of the input), and `ExecutionTime` (the time taken in milliseconds).

Your task is to write a Python script at `/home/user/analyze_perf.py` that processes this data and extracts statistical performance profiles. To speed up the analysis, your script must use the `multiprocessing` module to analyze the different functions in parallel.

For each unique `Function` in the dataset, calculate the following:
1. **Regression**: Perform a linear regression of `ExecutionTime` against `DataSize` using all available data for that function. Extract the `slope` of the fit.
2. **Distribution Fitting**: Filter the data for that function to only include rows where `DataSize == 1000`. Fit a log-normal distribution to the `ExecutionTime` values using `scipy.stats.lognorm.fit(data, floc=0)`. Extract the shape parameter (`s`) and the scale parameter (`scale`).

Your script must aggregate these results and save them to `/home/user/perf_summary.json`. The JSON file should contain a dictionary where the keys are the function names, and the values are objects with the keys `slope`, `lognorm_shape`, and `lognorm_scale`. The values should be floating-point numbers rounded to 4 decimal places.

For example, the output format should look like:
```json
{
  "init": {
    "slope": 0.5012,
    "lognorm_shape": 0.5123,
    "lognorm_scale": 512.1234
  },
  "compute": { ... }
}
```

Ensure your code is correct and runs without errors. You may use `pandas`, `scipy`, and `numpy`.