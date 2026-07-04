You are acting as a DevOps engineer debugging a custom log analysis tool written in C. The tool, located at `/home/user/log_analyzer.c`, is designed to parse web server logs, calculate an anomaly score for each IP address using an iterative algorithm, and output the results.

However, the tool is currently failing in two ways:
1. It produces incorrect anomaly scores for certain log entries, and upon inspection, it seems to mishandle some date formats. The log file contains dates in both `DD/MMM/YYYY` (e.g., 12/Oct/2023) and `YYYY-MM-DD` (e.g., 2023-10-12) formats. The tool's date parsing function needs to be fixed to handle both and convert them correctly to a standardized timestamp or just successfully parse the year, month, and day without failing.
2. The iterative anomaly scoring function sometimes fails to converge and exits prematurely or loops excessively. The function updates a score until the difference between iterations is less than an epsilon (0.001). However, there is a bug in how the convergence difference is calculated.

Your task:
1. Debug and fix the bugs in `/home/user/log_analyzer.c`. 
   - Fix the `parse_date` function to correctly extract the year from both `DD/MMM/YYYY` and `YYYY-MM-DD` formats.
   - Fix the `calculate_score` function so that the convergence check correctly uses the absolute difference between the old score and the new score.
2. Compile the tool using the provided `/home/user/Makefile`.
3. Run the compiled tool on `/home/user/server.log`. The tool takes the log file as the first argument and an output file as the second argument.
4. Output the results to `/home/user/results.txt`.

The output file `/home/user/results.txt` should contain lines in the format:
`IP: <ip_address>, Score: <final_score_rounded_to_3_decimal_places>`

Ensure that the program compiles without errors and generates the correct `results.txt`.