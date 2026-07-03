You have inherited an unfamiliar telemetry processing pipeline located at `/home/user/telemetry`. The pipeline is supposed to decompress raw binary logs using a custom C-extension and then parse the text to generate a summary JSON file. 

However, the nightly container job has been failing. 

Your tasks are:
1. **Container Log Inspection:** Review `/home/user/telemetry/container.log` to identify the cause of the recent crash.
2. **Fix the Build:** The C-extension (`fast_decomp`) fails to build due to a linker/compilation error. Fix the configuration so the extension compiles successfully using `python3 setup.py build_ext --inplace`.
3. **Format Parsing Edge-Case:** Fix the bug in `/home/user/telemetry/parser.py` that caused the pipeline to crash. The pipeline must correctly handle all edge cases present in the data without dropping any records.
4. **Execution:** Run the fixed pipeline: `python3 parser.py raw_data.bin summary.json`

Ensure that the final output `/home/user/telemetry/summary.json` is generated correctly and contains the parsed data from all records in the input file.