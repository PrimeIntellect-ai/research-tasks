As an automation specialist migrating our legacy data I/O workflows, I need you to replace an old, undocumented, compiled log processing utility with a modern Python script. 

The legacy binary is located at `/app/log_processor_legacy`. We don't have the source code, and it has been stripped of symbols. 

Your goal is to write a Python script at `/home/user/new_processor.py` that behaves EXACTLY like the legacy binary. It must read raw log lines from standard input (stdin) and output processed JSON lines to standard output (stdout), being bit-for-bit identical to the legacy output for any given input.

From my preliminary analysis, the legacy tool does the following data processing pipeline:
1. **Extraction**: It reads unstructured text lines formatted roughly as: `[TIMESTAMP] User:<USERNAME> Action:<ACTION> Metric:<VALUE>`
2. **Standardization**: It normalizes the `<ACTION>` string.
3. **Timestamp Alignment**: It parses various timestamp formats and aligns them to a standard UTC format.
4. **Rolling Statistics**: It calculates a rolling statistic (likely an average or sum) of the `<VALUE>` metric specific to each `<USERNAME>` over a certain window.

You need to use tools like `strings`, `objdump`, or simply treat `/app/log_processor_legacy` as a black box and send it various test inputs to deduce the exact formatting, window sizes, arithmetic rules, and JSON schema it uses. 

Create the replacement script at `/home/user/new_processor.py`. It should take no arguments, read continuously from `stdin` until EOF, and write to `stdout`. 

Make sure your script perfectly mimics the binary's behavior, including how it handles rounding, window tracking, and output formatting.