You are an IT support technician assigned to Ticket #8911. Our backend financial aggregation service crashed overnight.

You have been provided with the following files:
- `/home/user/aggregator.cpp`: The source code for the aggregator.
- `/home/user/data.csv`: The dataset it was processing when it crashed.
- `/home/user/memdump.bin`: A raw memory dump captured at the time of the crash.

Your objectives to resolve this ticket:

1. **Memory Dump Analysis**:
   Analyze the provided memory dump (`/home/user/memdump.bin`) and extract the specific error identifier string that was loaded in memory right before the crash. The error code starts with `ERR_CODE_`. Save this exact string into a new file at `/home/user/error_code.txt`.

2. **Format Parsing Edge-Case Repair**:
   The service crashes when parsing `/home/user/data.csv` due to a format parsing bug. Some rows are malformed (e.g., missing the amount field entirely or containing invalid characters). Fix `/home/user/aggregator.cpp` so that it safely ignores/skips any row where the amount field cannot be parsed as a number, instead of crashing. 

3. **Precision Loss Tracking**:
   The users reported that even before the crash, the total sum output by the service was slightly inaccurate due to precision loss when adding very small transactions to a massive running total. Identify and fix the precision loss issue in `/home/user/aggregator.cpp`. Ensure the final total is accurate.

4. **Verification**:
   Compile your fixed `aggregator.cpp` (e.g., using `g++ -o aggregator aggregator.cpp`) and run it against `data.csv`. 
   Take the final numerical total output by your fixed program (formatted to 2 decimal places, e.g., `12345678.90`) and save it to `/home/user/final_sum.txt`.

Ensure all requested output files (`/home/user/error_code.txt` and `/home/user/final_sum.txt`) are created exactly at those paths.