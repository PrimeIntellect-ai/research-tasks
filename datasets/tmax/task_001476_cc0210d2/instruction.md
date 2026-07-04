You are a support engineer investigating a bug in a data ingestion service. The service processes incoming binary logs asynchronously, but it has started hanging indefinitely in production. We have captured a batch of recent input files that triggers this issue.

Your objectives:
1. **Fix the Build**: The project is located in `/home/user/data_ingester`. Try to install it in editable mode (`pip install -e .`). It currently fails to build due to a syntax issue in the configuration. Diagnose and fix this so the package installs successfully.
2. **Reproduce and Diagnose**: Run the processor on the provided inputs: `python run_processor.py /home/user/inputs`. You will notice it hangs and never completes.
3. **Minimize the Failing Input**: One of the files in `/home/user/inputs` contains a malformed record that causes the hang. Identify which file it is, and use delta debugging/minimization techniques to find the exact minimum byte sequence that triggers the parser error leading to the hang. Save this minimal byte sequence to a file at `/home/user/minimized_crash.bin`.
4. **Fix the Hang**: Inspect the source code to find why a parser error causes the entire async application to hang. Fix the edge-case error handling in `/home/user/data_ingester/ingester/async_worker.py` so that even if a record is malformed, the async queues are managed properly and the program does not hang. 
5. **Verify**: Run `python run_processor.py /home/user/inputs` again. It should now complete and write a summary report to `/home/user/success.log`.

Ensure your fix allows the program to gracefully drop malformed records while continuing to process valid ones. Do not just remove the exception in the parser; fix the underlying async concurrency bug (task leak/hang) in the worker.