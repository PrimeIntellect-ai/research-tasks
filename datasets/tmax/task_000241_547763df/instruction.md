You are an on-call DevOps engineer. A critical background process that continuously records financial transaction data was running on your machine, but a junior developer accidentally ran `rm -rf` on the log directory `/home/user/data/`. 

The background process is still running, which means the deleted log file is still held open by the operating system.

Your task consists of three parts:

1. **Deleted File Recovery:** 
Locate the running background process (it's a python script named `transaction_generator.py`) and recover the contents of the deleted `transactions.log` file it is holding open. Save the recovered contents to exactly `/home/user/recovered_logs.txt`.

2. **Corrupted Input Handling:**
We have an aggregation script located at `/home/user/aggregator.py` that is supposed to read the log file, parse the JSON on each line, and sum up the `amount` field. However, the background process occasionally writes corrupted lines (e.g., truncated JSON or lines with unexpected null bytes). Modify `/home/user/aggregator.py` so that it gracefully skips any line that cannot be parsed as valid JSON, rather than crashing.

3. **Precision Loss Tracking & Fixing:**
The transactions contain a mix of very large baseline transfers (e.g., 100000000.0) and thousands of micro-transactions (e.g., 0.01). The current `/home/user/aggregator.py` uses standard Python `float` for summation, which is suffering from precision loss. Modify `/home/user/aggregator.py` to use Python's `decimal.Decimal` (or another exact mathematical approach) to compute the exact sum without floating-point inaccuracies. 

Once you have recovered the file and fixed the script, run the script against `/home/user/recovered_logs.txt`. 

Finally, write the exact, accurate total sum of all valid transactions to a file located at `/home/user/final_sum.txt`. The file should contain nothing but the exact numeric value (e.g., `100005000.25`).