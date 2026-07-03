You are an IT support technician responding to an escalated ticket. A backend data processing service has been frequently hanging and consuming all available memory until the OOM killer terminates it. 

We managed to capture a partial memory dump from the latest crashed process. The dump is located at `/home/user/ticket/core_dump.bin`. 

Your objectives are:
1. **Memory Dump Analysis**: Analyze `/home/user/ticket/core_dump.bin`. The developers log the last processed record just before operations in memory. Look for a string formatted exactly as `CRASH_CONTEXT: alias_name=<the_alias>`. Extract this alias name.
2. **Fix the Bug**: The code running this process is located at `/home/user/app/processor.py`. The `flatten_data` function is experiencing an infinite loop due to circular references in the aliases. Modify `flatten_data` in `/home/user/app/processor.py` so that it tracks visited aliases. If a circular reference (an alias that has already been encountered during the execution of the function) is detected, it must immediately raise a `ValueError("Circular reference detected")`.
3. **Regression Test Construction**: Create a minimal reproducible example and regression test in a new file `/home/user/app/test_regression.py`. 
    - You must use the `unittest` framework.
    - Write a test case that imports `flatten_data` from `processor.py`.
    - The test must call `flatten_data` with a dictionary containing the exact problematic alias extracted from the memory dump: `{"alias_of": "<the_alias>"}`.
    - The test must assert that a `ValueError` is raised.
4. **Verification**: Run your regression test using python's unittest module and redirect the output (both stdout and stderr) to `/home/user/app/test_output.txt`.

Ensure your test passes with your fixed code, demonstrating that the infinite loop is resolved and the error is correctly raised.