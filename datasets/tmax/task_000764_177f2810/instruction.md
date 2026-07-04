You are a data engineer tasked with migrating a legacy ETL pipeline. We have an old, undocumented data transformation component provided as a stripped binary at `/app/legacy_aggregator`. 

This binary is a crucial part of our stream processing pipeline. It reads UTF-8 encoded text from standard input (stdin), performs a specific rolling aggregation on the Unicode characters, writes the transformed data to standard output (stdout), and emits monitoring logs to standard error (stderr).

Because we need to update our infrastructure, we need the source code for this component. Your task is to:
1. Reverse-engineer the exact behavior of `/app/legacy_aggregator` by analyzing the binary or observing its input/output behavior.
2. Write a drop-in replacement program in C.
3. Save your source code at `/home/user/etl_transformer.c`.
4. Compile your code to an executable at `/home/user/etl_transformer` (e.g., using `gcc -O2 /home/user/etl_transformer.c -o /home/user/etl_transformer`).

Constraints & Hints:
- The input will strictly be valid UTF-8 text.
- The aggregation involves a sliding window over the Unicode code points.
- The program emits logging lines to stderr at specific intervals.
- Your replacement must be **bit-for-bit identical** in its stdout and stderr outputs for any given valid UTF-8 input stream.
- Do not hardcode responses to specific strings; you must implement the actual underlying algorithm so that it passes a rigorous fuzzing test against the legacy oracle.

Analyze the legacy binary, understand its window size, its aggregation math, and its logging frequency, and implement the exact same logic in C.