You have inherited an unfamiliar and partially broken video processing pipeline from a developer who abruptly left the company. The pipeline is located in `/home/user/pipeline/` and processes a reference video located at `/app/test_run.mp4`. 

Your goal is to fix the pipeline so it correctly generates a final calibrated event report at `/home/user/final_output.csv`. 

Here is what you know about the system and the issues you need to fix:

1. **Deleted Configuration Script**: Before leaving, the developer accidentally deleted a crucial awk processing script (`process_log.awk`) from a small ext4 filesystem image located at `/home/user/fs.img`. You must inspect this filesystem image, recover the deleted `process_log.awk` file, and place it in `/home/user/pipeline/`.

2. **Format Parsing Edge-Case**: The script `/home/user/pipeline/parse_timestamps.sh` extracts frame metadata using `ffprobe` and pipes it to the recovered awk script. However, it crashes or outputs `NaN` when it encounters timestamps with variable decimal precision or missing stream tags (a format parsing edge case). Debug and fix `parse_timestamps.sh` so it outputs clean, uniform frame data to a temporary file.

3. **Convergence Failure**: The pipeline uses `/home/user/pipeline/calibrate.sh` to determine an optimal brightness threshold for the extracted frames using a naive iterative adjustment loop. Currently, the loop oscillates infinitely (convergence failure) because of an integer division bug and incorrect bound updates in the Bash arithmetic. Fix the Bash script so the threshold converges properly and exits the loop.

4. **Query Result Debugging**: The final stage of the pipeline is `/home/user/pipeline/aggregate_queries.sh`. It takes the calibrated data, queries a local SQLite database (`/home/user/pipeline/events.db`), and generates the final CSV. The current SQL query contains a faulty JOIN that produces a Cartesian product, resulting in massively inflated event counts. Fix the query inside the Bash script so it correctly aggregates events per frame.

Once you have fixed all scripts, run the main orchestrator `/home/user/pipeline/run_all.sh`. It will generate `/home/user/final_output.csv`. 

The final CSV must have the format: `frame_index,timestamp,calibrated_threshold,event_count`. 
Your solution will be evaluated based on the Mean Squared Error (MSE) of your calculated thresholds and event counts compared to the ground truth.