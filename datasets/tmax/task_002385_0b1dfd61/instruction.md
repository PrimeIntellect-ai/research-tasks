You are an engineer tasked with investigating a critical failure in our data ingestion service. The service consists of a C-based backend processor and a Python daemon, but it is currently experiencing a severe memory leak and hanging indefinitely when processing certain datasets. 

To make matters worse, the primary input file was accidentally deleted from the filesystem by a junior operator!

Here is what you need to do to restore the service:

1. **Recover the Data**: The file `records.csv` was deleted from `/home/user/`, but it is still being held open in memory by a background process named `data_holder.py`. Inspect the system to find this process, extract the recovered file from memory via its file descriptors, and save the exact contents to `/home/user/recovered_records.csv`.

2. **Fix the C Processor**: 
   - The file `/home/user/processor.c` takes two arguments (`base` and `multiplier`), multiplies them, and prints the result. 
   - It works fine for small numbers but produces incorrect (negative) results on x86 architectures for large inputs due to a signed integer overflow. 
   - Fix `processor.c` so that it accurately computes and prints the multiplication of large valid inputs (using appropriate 64-bit data types). If any input argument is negative, it should continue to print `-1`.
   - Compile it using `gcc /home/user/processor.c -o /home/user/processor`.

3. **Fix the Python Daemon**: 
   - The file `/home/user/daemon.py` reads a CSV file, passes the values to the C processor, and aggregates the total sum. 
   - Currently, if the processor returns a negative number (which happens due to genuinely corrupted negative inputs in the CSV, or the unpatched integer overflow), `daemon.py` encounters an infinite loop and aggressively leaks memory.
   - Fix `daemon.py` so that it correctly handles negative results from the processor by entirely ignoring/skipping that record and continuing to the next one without leaking memory or getting stuck.

4. **Run and Report**: 
   - Modify `daemon.py` so that at the end of its execution, it writes the final valid aggregated total sum (as a single integer) to `/home/user/final_sum.txt`.
   - Run your fixed `daemon.py` against `/home/user/recovered_records.csv`.

**Environment details:**
- All your work should take place in `/home/user/`.
- Do not kill `data_holder.py` until you have successfully recovered the file, or the data will be lost forever.