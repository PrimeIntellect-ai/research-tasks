You are an automation specialist responsible for creating a high-performance data pipeline to process time-series sensor data from multiple factory floors. 

You have been given a set of wide-format CSV files located in `/home/user/sensor_data/`. Each file is named `floor_<N>.csv` and contains time-series data where the first column is the `timestamp` and the subsequent columns represent different sensor readings. The first row is the header.
Example:
```
timestamp,T1,H1
1000,22.5,50.1
1001,22.6,50.2
```

You also have a metadata file at `/home/user/metadata.csv` that maps each sensor ID to its type (without a header).
Example:
```
T1,temperature
H1,humidity
```

Your task is to orchestrate a multi-stage pipeline:
1. Write a C program at `/home/user/reshape.c` that reads a wide-format CSV from standard input and outputs a long-format CSV to standard output. 
   - The output format must be: `timestamp,sensor_id,value`
   - Do not print a header line in the output.
   - Ignore any blank lines.
2. Compile your C program to an executable at `/home/user/reshape`.
3. Write a bash script at `/home/user/workflow.sh` that:
   - Iterates over all `floor_*.csv` files in `/home/user/sensor_data/`.
   - Runs the `reshape` C program on each file in parallel (e.g., using background processes `&` and `wait`, or `xargs -P`).
   - Merges/joins the long-format results with `/home/user/metadata.csv` to add the sensor type.
   - Combines the data from all files into a single output file.
4. Execute `/home/user/workflow.sh`.

The final aggregated file must be saved to `/home/user/final_output.csv`.
The format of `/home/user/final_output.csv` must be:
`timestamp,sensor_id,sensor_type,value`
(e.g., `1000,T1,temperature,22.5`)

Important constraints for the final output:
- It must not contain any headers.
- It must be sorted numerically by `timestamp` (ascending), and then alphabetically by `sensor_id` (ascending).
- Use standard bash tools (like `sort`, `join`, `awk`, etc.) in your script alongside the C program.