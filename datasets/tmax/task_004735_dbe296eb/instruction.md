You are a DevOps engineer tasked with resolving a critical issue in our log processing pipeline. 

We use a proprietary compiled tool located at `/app/log_analyzer` to calculate anomaly scores for our access logs. Recently, the pipeline has been experiencing severe slowdowns and timeouts. We suspect that certain malformed log entries are causing the internal algorithm of `/app/log_analyzer` to suffer from a convergence failure, leading to near-infinite loops.

The tool reads from standard input (one log entry per line) and prints the anomaly score (a float) to standard output. 

Your task is to:
1. Write a fuzzing script to generate variations of typical access logs and pipe them to `/app/log_analyzer` to identify the exact pattern or anomaly causing the convergence failure (the tool hangs or takes >1 second for a single line).
2. Create a regression test suite in `/home/user/tests/` to capture these failing cases.
3. Write a Python script at `/home/user/safe_analyzer.py` that reads log lines from standard input, identifies and repairs/filters the problematic malformed lines (by removing the specific characters or fields causing the hang, while keeping the rest of the line intact), and then passes the sanitized lines to `/app/log_analyzer` via a subprocess to get the score. The script should print the score for each line to standard output.

We have provided a sample of standard logs in `/home/user/sample_logs.txt`. 

Your `safe_analyzer.py` must be robust. We will test it against a large, held-out dataset of logs. It must process the logs significantly faster than the raw binary (by avoiding the hangs) while maintaining accurate anomaly scores for the valid parts of the logs.