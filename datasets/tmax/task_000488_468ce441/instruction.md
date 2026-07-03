You are a performance engineer tasked with optimizing a log processing pipeline. 

In `/home/user/perf_task`, you will find:
1. `legacy_bin`: A compiled binary (source code lost) that processes an integer and computes a specific metric.
2. `slow_processor.c`: A recent attempt to rewrite `legacy_bin` in C. It reads log lines from standard input, extracts a value, computes the metric, and prints the formatted result. However, `slow_processor.c` has a severe performance bottleneck (it uses a slow algorithm) and contains a bug in its formula implementation that causes it to fail or overflow on large inputs.
3. `fuzz_test.sh`: A script that generates random large integers, passes them to a binary, and compares the output against `legacy_bin`.
4. `logs/`: A directory containing unordered log files from different microservices (`svcA.log`, `svcB.log`, `svcC.log`).

Your objectives:
1. **Reverse Engineer & Correct:** Determine the exact mathematical formula `legacy_bin` is using (hint: it calculates a well-known mathematical sequence). 
2. **Optimize:** Fix `slow_processor.c` by replacing the bottleneck with an $O(1)$ formula implementation. Ensure it uses the correct data types (`uint64_t`) to prevent overflows for large inputs (up to $4 \times 10^9$).
3. **Compile & Fuzz:** Compile your fixed code to `/home/user/perf_task/fast_processor`. Ensure it passes `./fuzz_test.sh ./fast_processor` without any mismatches or timeouts.
4. **Log Timeline Reconstruction:** The logs in `logs/` contain lines in the format: `YYYY-MM-DD HH:MM:SS [ServiceName] val=N`. Pass the contents of all log files through your `fast_processor`. 
5. Merge the outputs and chronologically sort them by timestamp. Save the final sorted output to `/home/user/perf_task/unified_timeline.log`.

The output format of your `fast_processor` (and thus `unified_timeline.log`) must be exactly:
`YYYY-MM-DD HH:MM:SS | ServiceName | N | ComputedMetric`

Note: Do not modify `legacy_bin` or `fuzz_test.sh`. You only need to edit `slow_processor.c`, compile it, and generate the final log file.