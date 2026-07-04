You are an on-call engineer, and your pager just went off at 3 AM. The automated trading pipeline has crashed, and the system is producing statistically anomalous results before the crashes.

You have been granted access to the affected environment. The pipeline directory is `/home/user/pipeline`. 

Here is what we know:
1. The pipeline consists of a Python script `/home/user/pipeline/process.py` that delegates heavy numerical processing to a C shared library `/home/user/pipeline/libcalc.so` (compiled from `/home/user/pipeline/calc.c`).
2. Before the system fully crashed, it dumped the application's memory space to `/home/user/pipeline/memdump.bin`. 
3. The logs indicate an anomaly caused by a specific transaction ID just before the crash, but the ID wasn't logged.

Your tasks:
1. **Memory Dump Analysis:** Extract the failing transaction ID from `/home/user/pipeline/memdump.bin`. The transaction IDs always start with `TXN-` followed by 8 alphanumeric characters. Save ONLY the exact transaction ID string to `/home/user/pipeline/bad_txn.txt`.
2. **Fix the Off-by-One:** Inspect `/home/user/pipeline/calc.c`. There is a boundary condition (off-by-one error) causing an out-of-bounds memory read, which pulls in garbage data and contributes to statistical anomalies. Fix the loop bounds.
3. **Fix Numerical Precision Loss:** The accumulator in `calc.c` suffers from precision loss when summing many values. Identify the precision bottleneck in the C code and upgrade the variable types to double precision to prevent numerical instability.
4. **Recompile and Run:** 
   - Recompile the C extension: `gcc -shared -o /home/user/pipeline/libcalc.so -fPIC /home/user/pipeline/calc.c`
   - Run the processing script: `python3 /home/user/pipeline/process.py`
   - Ensure the script runs successfully and writes its output to `/home/user/pipeline/results.json`.

Do not change the inputs in `process.py`. Only fix the bugs in `calc.c`, extract the transaction ID, recompile, and generate the final output.