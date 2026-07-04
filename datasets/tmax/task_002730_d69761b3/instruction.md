You are a data analyst working on server performance metrics. You have been given a raw dataset of server latencies and a partially complete Python script that is supposed to analyze the data, but it is failing to run correctly in our headless Linux environment.

Your objective is to build a reproducible Bash/Python pipeline to process this data, perform statistical testing, and generate a plot.

**Initial Setup:**
You have two files in your home directory (`/home/user/`):
1. `raw_latency_data.csv`: A CSV file with columns `timestamp,server_group,latency_ms`. There are two server groups: `A` and `B`.
2. `analyze_and_plot.py`: A Python script that performs an independent two-sample t-test between the latencies of group A and group B, and generates a boxplot.

**Your Tasks:**
1. **Create an ETL Bash Script:** Write a script at `/home/user/etl.sh` that reads `raw_latency_data.csv` and calculates the average `latency_ms` for each `server_group`. The script must output a new CSV file at `/home/user/summary.csv` with exactly two columns: `server_group,avg_latency` (include the header, and format the average to exactly 2 decimal places). Use standard Bash tools (like `awk`) for this, do not use Python for this specific step.

2. **Fix the Python Script:** The provided `/home/user/analyze_and_plot.py` script is currently broken. It was written on a desktop and uses `plt.show()`, which hangs or crashes in our headless testing environment, and it fails to save the plot correctly. Modify the script so that:
   - It runs successfully without a graphical display.
   - It writes the calculated t-test p-value to `/home/user/p_value.txt` (just the numeric value, rounded to 4 decimal places).
   - It successfully saves the plot to `/home/user/latency_plot.png`.

3. **Orchestrate the Pipeline:** Create a master executable script at `/home/user/run_pipeline.sh` that:
   - First executes `./etl.sh`
   - Then executes `python3 analyze_and_plot.py`

**Expected Final State:**
After running `/home/user/run_pipeline.sh`, the following files must exist and be correct:
- `/home/user/summary.csv` (created by the Bash script)
- `/home/user/p_value.txt` (created by the Python script)
- `/home/user/latency_plot.png` (created by the Python script)