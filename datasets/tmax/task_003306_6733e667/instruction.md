Wake up! It's 3 AM and you're on call. The upstream metrics emitter is crashing our downstream analytics pipeline. 

Here is the situation:
1. A Python daemon called `metrics_emitter.py` was writing critical telemetry data to `/tmp/metrics.dat`.
2. A faulty log-rotation cronjob accidentally deleted `/tmp/metrics.dat` from the filesystem about an hour ago. However, the daemon is still running and holding the file descriptor open.
3. The downstream Rust parsing service located at `/home/user/parser` is failing to process this data format due to a bug.

Your tasks are:
1. **Recover the deleted file**: Extract the data from the running `metrics_emitter.py` process's open file descriptor and save it to `/home/user/recovered.dat`.
2. **Fix the parser**: The Rust parser at `/home/user/parser` is failing with an assertion error. There is an off-by-one boundary allocation error when sizing the buffer for the incoming variable-length records. Fix the buffer allocation logic in `src/main.rs` so that the intermediate assertion passes.
3. **Parse the data**: Recompile the Rust parser and run it against your recovered data file:
   `cargo run --manifest-path /home/user/parser/Cargo.toml -- /home/user/recovered.dat > /home/user/final_metrics.txt`

The format of the final output file `/home/user/final_metrics.txt` should be a comma-separated list of the parsed strings. Fix the code, recover the data, and generate the final output file.