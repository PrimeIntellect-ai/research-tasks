As an automation specialist, you are building a high-performance data processing pipeline in C to handle a continuous stream of telemetry records.

We have a proprietary sensor simulator located at `/app/data_gen`. This is a stripped Linux binary that outputs exactly 2,000,000 binary records to `stdout`.

Each binary record is exactly 36 bytes and has the following tightly packed structure (little-endian):
- `timestamp`: 64-bit unsigned integer (8 bytes)
- `user_id`: 32-bit unsigned integer (4 bytes)
- `value`: 64-bit IEEE 754 floating-point number (8 bytes)
- `hash`: 16-byte array (16 bytes)

You also have a mapping file at `/app/users.csv` containing `user_id,group_id` (both are integers). 

Your task is to write a C program (e.g., `/home/user/processor.c`) that reads the binary stream from `stdin` and performs the following operations:
1. **Large-file streaming**: Read the binary stream efficiently.
2. **Hash-based deduplication**: Maintain a rolling window of the last 5,000 valid (non-duplicate) `hash`es seen. If an incoming record's `hash` exactly matches any hash currently in this window, drop the record entirely.
3. **Joins**: For each valid record, look up the `group_id` for the record's `user_id` using the data from `/app/users.csv`. If a `user_id` is not found in the CSV, default its `group_id` to `0`.
4. **Rolling statistics**: For each `group_id`, maintain the Simple Moving Average (SMA) of the `value` field for the last 10 valid records belonging to that `group_id`. If fewer than 10 records have been seen for a group, compute the average of the available values.
5. **Output**: For every valid (non-duplicate) record, output a line to `stdout` in the format: `timestamp,group_id,sma`. The `sma` should be printed to 4 decimal places.

Compile your C program with `-O3` and run the pipeline, saving the output to `/home/user/output.csv`. For example:
`/app/data_gen | /home/user/processor > /home/user/output.csv`

Ensure your code handles the data accurately and efficiently.