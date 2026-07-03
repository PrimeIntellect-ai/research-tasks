You are an AI assistant helping a machine learning engineer prepare training data and benchmark a mock inference process. The engineer has been running into issues where their visualization scripts produce blank plots due to headless environment misconfigurations, so your solution must explicitly handle generating plots in a terminal environment.

Your task is to write a script in the language of your choice that performs data joining, aggregation, inference benchmarking, and visualization.

Here is the setup:
You have two datasets in `/home/user/`:
1. `demographics.csv`: Contains `user_id` and `age`.
2. `activity.csv`: Contains `uid`, `event_type`, and `latency_ms`.

Write and execute a script that does the following:
1. **Multi-source Data Joining & Aggregation**: 
   - Load both datasets.
   - Join them based on `user_id` and `uid`.
   - Aggregate the activity data per user to calculate the total count of events (`event_count`) and the mean latency (`avg_latency`).
   - Save the processed data to `/home/user/training_data.csv`. The CSV should have exactly these columns in this order: `user_id`, `age`, `event_count`, `avg_latency`. The rows must be sorted by `user_id` in ascending order.

2. **Inference Performance Benchmarking**:
   - Write a dummy inference loop that iterates through every row of your aggregated dataset 10,000 times.
   - In each inner iteration, multiply the user's `age` by their `avg_latency`.
   - Measure the total wall-clock time taken to execute this entire loop (all 10,000 passes).
   - Save a file `/home/user/report.json` with the following schema:
     `{"total_inference_time_seconds": <float>, "row_count": <int>}`

3. **Visualization**:
   - Create a scatter plot comparing `age` (x-axis) and `avg_latency` (y-axis) from the aggregated dataset.
   - Save the plot as `/home/user/plot.png`.
   - *Requirement*: Ensure your code successfully generates and saves the image file in a headless terminal environment (e.g., if using Python's matplotlib, ensure the correct non-interactive backend is configured so it doesn't crash or save a blank plot).

You are free to use shell commands or write a script in Python, Ruby, Perl, etc. to accomplish this. Just ensure all output files (`training_data.csv`, `report.json`, `plot.png`) are correctly created in `/home/user/`.