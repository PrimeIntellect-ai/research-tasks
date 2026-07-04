You are a performance engineer working on a high-throughput latency monitoring service. Your team relies on a custom sliding window statistics module written in Python to calculate real-time latency percentiles.

However, the monitoring dashboard is occasionally showing spiked or incorrect percentile values, especially when the sliding window reaches its maximum capacity. 

You have been provided with the source code for the statistics module located at `/home/user/workspace/stats_buffer.py`. 

Upon initial investigation, your team suspects there are two distinct bugs:
1. **Boundary condition / Off-by-one error:** When the ring buffer reaches its maximum size and needs to overwrite the oldest latency value, it is not overwriting the correct index.
2. **Formula implementation error:** The mathematical formula used to calculate the exact percentile rank index in the sorted array is slightly incorrect, leading to wrong interpolations. 

Your task:
1. Debug and fix both issues in `/home/user/workspace/stats_buffer.py`. Do not change the class name or method signatures.
    - For the percentile formula, use the standard method where the rank `k` is calculated as `(N - 1) * (p / 100.0)` where `N` is the number of elements.
    - For the ring buffer, ensure that when appending to a full buffer, the absolute oldest element is replaced, and the oldest element pointer is properly advanced.
2. Write a regression test script at `/home/user/workspace/test_stats.py` that imports `SlidingWindowStats` from `stats_buffer`. This test script must explicitly test both the ring buffer wrap-around logic and the percentile calculation.
3. If all tests in your script pass, the script must write the exact string `SUCCESS` to the file `/home/user/workspace/verification.log`. If they fail, write `FAILED`.

Ensure your code is correct and handles edge cases appropriately.