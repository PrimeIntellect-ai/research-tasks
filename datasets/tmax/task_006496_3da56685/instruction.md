You are an AI assistant helping a scientific researcher organize and process telemetry datasets. 

The researcher has two datasets from different sensor arrays:
1. `/home/user/sensor_alpha.csv` contains spatial coordinates: `id, timestamp, x_coord, y_coord, z_coord`
2. `/home/user/sensor_beta.csv` contains environmental data: `id, timestamp, temperature, pressure`

Please perform the following data processing pipeline using Python:
1. **Multi-source Data Joining:** Merge the two datasets on both `id` and `timestamp` (inner join).
2. **Feature Engineering:**
   - Create a new feature `magnitude` which is the Euclidean distance from the origin for the spatial coordinates: $\sqrt{x^2 + y^2 + z^2}$.
   - Create a new feature `temp_norm` which is the natural logarithm of `temperature`.
3. **Feature Selection:** Filter the dataset to only include the following columns: `id`, `timestamp`, `magnitude`, `temp_norm`, and `pressure`.
4. **Large-scale Data Storage:** Save the resulting joined and engineered dataset as a Snappy-compressed Parquet file at `/home/user/processed_data.parquet`.
5. **Summary Reporting:** Calculate the mean of the new `magnitude` and `temp_norm` columns. Write these values to `/home/user/summary.txt` in exactly this format (rounded to exactly 4 decimal places):
```
Mean Magnitude: [value]
Mean Temp Norm: [value]
```

Ensure your Python script runs successfully and produces both `/home/user/processed_data.parquet` and `/home/user/summary.txt`.