You are a data scientist handling a batch of messy sensor data. Your task is to build a multi-stage data processing pipeline in Go.

You have been given a raw CSV dataset located at `/home/user/sensor_data.csv`.
The CSV has the following headers:
`timestamp,sensor_id,reading,error_code`

Write a Go program at `/home/user/pipeline.go` that implements the following data cleaning and aggregation pipeline:

**Stage 1: Error Filtering**
Read the CSV file and drop any rows where the `error_code` column is not empty. 

**Stage 2: Range Normalization**
From the remaining rows, drop any rows where the `reading` value (a float) is strictly less than 0.0 or strictly greater than 1000.0.

**Stage 3: Aggregation**
For the valid rows that pass through both filters, aggregate the data by `sensor_id`. Calculate the total count of valid readings and the average (mean) reading for each sensor.

**Stage 4: JSON Export**
Write the aggregated statistics to a file named `/home/user/clean_summary.json`.
The output must be a JSON object where the keys are the `sensor_id` strings, and the values are objects containing `average` (a float) and `count` (an integer).

Example expected structure for `/home/user/clean_summary.json`:
```json
{
  "alpha": {
    "average": 150.5,
    "count": 2
  },
  "beta": {
    "average": 45.0,
    "count": 1
  }
}
```

Constraints:
- You must write the solution in Go.
- Execute your Go program to generate the `/home/user/clean_summary.json` file.
- Do not round the averages (let Go's default JSON marshaling handle the float64 representation).
- Ensure the JSON file is properly formatted and valid.