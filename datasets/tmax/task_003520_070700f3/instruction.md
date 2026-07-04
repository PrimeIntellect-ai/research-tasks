You are tasked with rewriting a legacy Configuration Change Tracker utility in C. The old utility is provided as a stripped binary at `/app/oracle_tracker`, but we have lost the source code and need a maintainable C implementation that behaves exactly identically.

The utility reads a continuous stream of configuration changes from `stdin` (representing a time-series of events) and writes an enriched log to `stdout`.

Input Format (Tab-separated values on each line):
`<Timestamp> \t <ConfigKey> \t <HexEncodedValue> \n`
- `Timestamp`: A strictly monotonically increasing integer (Unix timestamp).
- `ConfigKey`: An alphanumeric string (max 32 chars).
- `HexEncodedValue`: A hex-encoded string representing the new configuration value (e.g., `4f4e` for "ON").

Expected Output Format (Tab-separated values on each line):
`<Timestamp> \t <ConfigKey> \t <NormalizedValue> \t <RecentChangeCount> \n`
- `Timestamp` and `ConfigKey`: Passed through unmodified.
- `NormalizedValue`: The `HexEncodedValue` decoded into ASCII characters, and then entirely normalized to lowercase.
- `RecentChangeCount`: An integer representing the total number of times this specific `ConfigKey` has appeared in the stream within a 60-second trailing rolling window (inclusive). Meaning, you count all occurrences of this `ConfigKey` where `event_time >= current_time - 60`.

Requirements:
1. Write the source code in `/home/user/tracker.c`.
2. Compile it to the executable `/home/user/tracker` using `gcc -O2 /home/user/tracker.c -o /home/user/tracker`.
3. Your compiled program must read from `stdin` until EOF and stream the results to `stdout`.
4. It must perfectly match the output of `/app/oracle_tracker` for any valid input. You can use the provided oracle to verify your edge cases.