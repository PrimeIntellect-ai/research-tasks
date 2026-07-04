You are tasked with building a C-based metrics aggregation tool for a configuration management system. The system receives drift metrics from various servers at irregular intervals, spanning two different formats: CSV and JSON Lines (JSONL). 

Your objective is to write a C program that reads these files, unifies the data, resamples it to a regular 1-second interval, fills gaps, calculates a rolling average, and outputs the result to a strict binary format.

### Input Data
You will process two input files located in `/home/user/`:
1. `/home/user/updates.csv`: Contains comma-separated values with the header `timestamp,metric_id,value`.
2. `/home/user/updates.jsonl`: Contains JSON Lines, where each line is strictly formatted as `{"ts": <int>, "id": <int>, "val": <double>}`.

There are only two metrics of interest: `metric_id` 1 and `metric_id` 2. Timestamps (`ts` or `timestamp`) are integers representing seconds. Values (`val` or `value`) are doubles.

### Processing Requirements
Write a C program located at `/home/user/config_tracker.c`. The program must perform the following:
1. **Multi-format Reading:** Read both input files and merge the updates.
2. **Resampling & Gap-Filling:** Produce an output record for *every integer second* from the minimum timestamp found across both files to the maximum timestamp found (inclusive). 
   - If multiple updates for the same `metric_id` occur at the exact same timestamp, use the latest one encountered (process CSV first, then JSONL, keeping the JSONL value if there's a tie at the exact same timestamp).
   - **Gap-filling:** Use Last-Observation-Carried-Forward (LOCF). If a metric has no observation at a given second, carry forward the most recent previous value. If no previous value exists for a metric (i.e., before its first observation), use `0.0`.
3. **Rolling Aggregation:** For both metrics, calculate a 5-second moving average (MA5). This average must include the current second and the up-to 4 preceding seconds (using the resampled, gap-filled values). If fewer than 5 seconds of history exist (at the beginning of the timeline), average over the available seconds.

### Output Format
The program must write the processed data to a binary file at `/home/user/metrics_out.bin`. 
The file must contain a sequential array of the following C struct (tightly packed, native endianness, standard alignment for x86_64 Linux):

```c
struct OutputRecord {
    int timestamp;
    double metric1_val;
    double metric1_ma5;
    double metric2_val;
    double metric2_ma5;
};
```
The records must be sorted by `timestamp` in ascending order.

### Instructions
1. Write the C code in `/home/user/config_tracker.c`.
2. Do not use external libraries that require root/sudo installation (standard C library only). You can parse the strictly formatted JSONL using standard string functions (`sscanf`, `strstr`, etc.).
3. Compile the code to `/home/user/config_tracker` and execute it to generate the binary file.