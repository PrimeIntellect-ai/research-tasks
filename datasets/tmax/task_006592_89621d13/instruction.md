You are an AI assistant helping a data researcher fix a bug in their data processing pipeline.

The researcher is organizing a dataset of sensor readings, preparing it for downstream machine learning tasks. The dataset is located at `/home/user/data.csv`. It contains three columns: `id`, `timestamp`, and `value`. 

Occasionally, the sensors drop their connection, and the `id` field is logged as the literal string `"NaN"`. The researcher wrote a Rust program located in `/home/user/anomaly_detector` to read this CSV and calculate the simple linear regression slope of `value` over `timestamp` for each sensor ID. 

However, there is a silent numerical accuracy bug in the Rust pipeline. The code currently parses the `id` column as an `f64` (which successfully parses `"NaN"` as `f64::NAN`) and then casts it to an `i32`. In Rust, casting `f64::NAN` to `i32` evaluates to `0`. As a result, the corrupted `"NaN"` records are being silently merged with the legitimate readings from sensor ID `0`, heavily skewing the regression slope for sensor `0`.

Your task is to:
1. Fix the bug in `/home/user/anomaly_detector/src/main.rs`. The program should completely ignore (skip) any row where the `id` is `"NaN"` (or evaluates to `f64::NAN`), rather than merging it with ID `0`.
2. Compile and run the Rust program to verify it calculates the correct slopes.
3. Save the correct slopes for sensor ID 0 and sensor ID 1 to a file named `/home/user/slopes.txt`. 

The format of `/home/user/slopes.txt` must be exactly:
```
0: <slope_for_id_0>
1: <slope_for_id_1>
```
Keep the precision to at least 1 decimal place (e.g., `2.0`).

You may use any terminal tools to explore the data, but the fix must be implemented in the provided Rust project.