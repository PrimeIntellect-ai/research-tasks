You have inherited a fragile data processing pipeline written in Bash that recently stopped working correctly. The pipeline script is located at `/home/user/pipeline/run_pipeline.sh`. It relies on a custom binary called `log_parser` to process several log files in the `/home/user/pipeline/data/` directory.

However, the pipeline currently suffers from several issues:
1. **Dependency Conflict:** The script attempts to set up the environment, but it sets the `LD_LIBRARY_PATH` incorrectly, causing the `log_parser` binary to use a legacy, incompatible version of a shared library (`libutils.so`). This causes unexpected behavior or linker errors.
2. **Race Condition:** The script uses background jobs (`&`) to process the log files in parallel, but all jobs write concurrently to a single shared file (`/home/user/pipeline/output.txt`) using `>>`. This race condition causes corrupted lines and missing data.
3. **Core Dump / Unhandled Edge Cases:** One or more of the log files contains corrupted edge-case data (a line containing the exact string `"FATAL_CORRUPTION"`). When `log_parser` encounters this, it crashes and prints a stack trace to standard error.

Your task is to debug and fix the pipeline:
1. Analyze the pipeline and environment to resolve the library dependency conflict so `log_parser` uses the correct library located in `/home/user/pipeline/lib_modern/`.
2. Analyze the error logs/stack traces to identify the corrupted input data. 
3. Create a fixed version of the pipeline script named `/home/user/pipeline/run_pipeline_fixed.sh`.
4. In your fixed script, add an **assertion-based validation step** (pure Bash) that checks each file for the string `"FATAL_CORRUPTION"` *before* passing it to `log_parser`. If the file contains this string, the script should print `Skipping corrupt file: <filename>` to standard output and skip processing that file.
5. In your fixed script, resolve the race condition so that the parallel background processing does not result in interleaved or missing lines. (Hint: writing to separate intermediate files and assembling them at the end, or using proper locking).
6. Execute your fixed script. The final, correctly processed and assembled output must be saved to `/home/user/pipeline/output_final.txt`. It should contain the processed lines from all valid log files.

Ensure your fixed script is executable and completely standalone. Do not modify the `log_parser` binary or the shared libraries themselves.