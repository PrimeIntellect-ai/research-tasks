It's 3:00 AM and you've just been paged. The billing team reports that their end-of-day data processing pipeline is mysteriously dropping the final transaction from every batch file, leading to revenue discrepancies. 

The service responsible is a Go-based data transformer called `tx-processor`.

Here is the situation:
- The source code is located at `/home/user/tx-processor.go`.
- The currently running (buggy) binary is at `/home/user/tx-processor`.
- A sample input batch file is located at `/home/user/batch_data.csv`.

Your objectives are:
1. **System Call Tracing**: The billing team is skeptical that the Go application is at fault and blames the filesystem. Prove the app is at fault by tracing the `read` and `write` system calls. Run `tx-processor` against `/home/user/batch_data.csv`, redirecting standard output to `/dev/null`. Use `strace` to capture only `read` and `write` syscalls and save the trace output to `/home/user/strace.log`.
2. **Data Transformation Diff Analysis**: Compare the input and the buggy output. You will notice the missing data and the applied transformations.
3. **Boundary Condition Repair**: Identify the off-by-one error or boundary condition bug in `/home/user/tx-processor.go`. Fix the source code.
4. **Recompile & Process**: Recompile the binary to `/home/user/tx-processor` and process `/home/user/batch_data.csv`. Save the correct, complete output to `/home/user/batch_data_fixed.csv`.

Once you have generated `/home/user/strace.log`, fixed the code, and produced `/home/user/batch_data_fixed.csv` containing all processed lines, you are done.