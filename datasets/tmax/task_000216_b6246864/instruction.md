You are a mobile build engineer tasked with optimizing the telemetry data pipeline for our continuous integration servers. Currently, our CI servers generate massive custom build traces, and our existing Python parser takes too long to process them, causing delays in build metric dashboards.

Your task is to write a high-performance C parser using a state machine, configure its build system, link it with our internal statistics library, and benchmark it against the legacy Python parser.

**Environment Setup & Requirements:**
1. Work in `/home/user/build_metrics/`.
2. A static library `libstats.a` and its header `stats.h` have been provided in `/home/user/build_metrics/lib/` and `/home/user/build_metrics/include/` respectively.
   The header contains:
   ```c
   void stats_init(void);
   void stats_add(double value);
   double stats_get_mean(void);
   double stats_get_variance(void);
   ```
3. A large log file is located at `/home/user/build_metrics/build_trace.log`. 
   The log contains interleaved lines. You only care about lines with the following exact formats:
   - `START_TRACE::[target_name]::[timestamp_in_ms]`
   - `END_TRACE::[target_name]::[timestamp_in_ms]`
   Other lines (warnings, info logs) should be ignored. `target_name` will not contain spaces or `::`.
4. The legacy parser is at `/home/user/build_metrics/slow_parser.py`.

**Task Instructions:**
1. **Write the C Parser (`fast_parser.c`)**:
   - Write a high-performance parser in C using a state-machine character-by-character parsing approach (do not use slow string allocations or heavy regex).
   - Track the duration (`END_TRACE` timestamp - `START_TRACE` timestamp) for all targets whose `target_name` begins with `mobile_module_`.
   - Feed these durations (as doubles) into the `stats` library (call `stats_init()` first, then `stats_add(duration)` for each matched target).
   - Print the final mean and variance to standard output in the format: `Mean: <value>, Variance: <value>`.

2. **Configure the Build**:
   - Create a `Makefile` in `/home/user/build_metrics/` that compiles `fast_parser.c` into an executable named `fast_parser`.
   - Ensure it links statically against `libstats.a` using the provided include and lib directories. Use `-O3` optimization.

3. **Benchmarking**:
   - Run both `slow_parser.py` and your `fast_parser` on `build_trace.log`.
   - Measure the execution time of both.
   - Create a report file at `/home/user/build_metrics/report.txt` containing exactly three lines:
     ```
     Mean: <calculated_mean_formatted_to_2_decimal_places>
     Variance: <calculated_variance_formatted_to_2_decimal_places>
     Fast Parser was Faster: <True/False>
     ```