You are a data scientist troubleshooting an ETL pipeline that recently failed. Due to a retry bug, the upstream job produced a massive stream of JSON records with duplicate entries. We also need to normalize these records using a specific feature extracted from a raw dataset video.

Your task is to create a Go program that acts as a robust, streaming ETL filter. 

**Video Feature Extraction:**
There is a raw video file located at `/app/traffic_cam.mp4`. 
You must analyze this video to find the exact total number of frames. This integer value will be used as the `SCALING_FACTOR` in your program.

**The ETL Filter Program:**
Write a Go program at `/home/user/etl_cleaner.go` and compile it to `/home/user/cleaner`. 
This executable will be tested in a pipeline by piping a continuous stream of data into its standard input (`stdin`) and reading from standard output (`stdout`).

**Data Processing Rules:**
1. **Streaming Input**: Read JSON lines from `stdin`. Each valid line represents a record with the following schema:
   `{"id": "some-string", "value": 123.45}`
2. **Deduplication**: The pipeline upstream failed and sent duplicates. Maintain a registry of seen `id`s. If a record has an `id` that has already been processed during the execution, it must be completely ignored (dropped).
3. **Transformation**: For every unique, valid record, calculate a new field: `scaled_value = value * SCALING_FACTOR`.
4. **Output**: Write the transformed record to `stdout` as a JSON line with exactly this structure:
   `{"id":"<id>","scaled_value":<calculated>,"value":<original>}` (The struct fields should be output in alphabetical order by their JSON keys, which happens naturally if you define your Go struct fields alphabetically: `Id`, `ScaledValue`, `Value`).
5. **Validation/Logging**: If a line cannot be parsed as valid JSON or is missing the `id` field, drop the record and print `invalid record` to `stderr` with a newline.

**Constraints:**
- The program must process data streamingly (do not load the entire `stdin` into memory at once).
- Do not round the `scaled_value`, just let Go's standard float64 JSON serialization handle it.
- Your final executable must be located exactly at `/home/user/cleaner`.

Make sure to find the frame count of the video first, hardcode or pass it to your Go program, and ensure your program behaves exactly as specified.