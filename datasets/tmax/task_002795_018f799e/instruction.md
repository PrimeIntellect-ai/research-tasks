You are a DevOps engineer debugging a multi-language audio processing pipeline.

The pipeline is located in `/home/user/pipeline/`. It analyzes an audio diagnostic recording located at `/app/diagnostic_recording.wav`. 
The pipeline consists of three stages orchestrated by `/home/user/pipeline/run.sh`:
1. `extract.py`: Reads the WAV file and outputs raw floating-point samples to standard output.
2. `aggregate.cpp`: Reads the raw samples from stdin, calculates a cumulative energy metric and a rolling average, and prints the result to stdout. It also prints intermediate state tracing logs.
3. `analyze.py`: Reads the aggregated metrics from stdin and writes the final sequence to `/home/user/pipeline/final_output.txt`.

Currently, the pipeline is failing. When you run `./run.sh`, `analyze.py` throws a traceback because it receives unexpected text instead of numeric data. 

Additionally, we have noticed in earlier tests that even when the pipeline completes, the final calculated energy metrics drift significantly from the theoretical true values due to floating-point precision issues in the aggregation stage.

Your tasks:
1. Debug the traceback in the pipeline. You will likely need to analyze the intermediate logging of `aggregate.cpp` and ensure that debug logs do not pollute the data stream.
2. Trace the intermediate states to find where precision is lost. Repair the floating-point precision issue in `aggregate.cpp` so that it computes the cumulative metrics with high precision (at least 64-bit IEEE 754 precision).
3. Ensure the final output file `/home/user/pipeline/final_output.txt` is successfully generated and contains the precise line-by-line float values.

Do not change the mathematical logic of the aggregation, only fix the data types, formatting, and logging stream issues.

Run `./run.sh` to begin your diagnosis.