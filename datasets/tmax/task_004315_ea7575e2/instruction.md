You are a log analyst investigating a series of anomalies in a remote server farm. The only data we recovered from the crashed monitoring system is a raw video dump, `/app/server_monitor.mp4`, which encoded text-based log telemetry in its subtitle stream to save bandwidth.

Your goal is to build a C++ data processing tool and a bash pipeline to extract and analyze this telemetry. 

**Step 1: Data Extraction**
Use `ffmpeg` (which is preinstalled) to extract the subtitle track from `/app/server_monitor.mp4`. The extracted data will contain lines of telemetry in a specific wide format. 

**Step 2: C++ Log Processor**
Write a C++ program and compile it to `/home/user/processor`. This program must be highly efficient (capable of large-file streaming) and strictly read from standard input (`stdin`) and write to standard output (`stdout`).

Input Format (Wide Format):
Each line in the input will be structured as:
`TIMESTAMP REGEX_PATTERN N VAL_1 VAL_2 ... VAL_N`
- `TIMESTAMP`: An integer representing the Unix timestamp.
- `REGEX_PATTERN`: A standard ECMA POSIX regex pattern string (without spaces).
- `N`: The integer number of sensor readings that follow.
- `VAL_i`: Floating-point sensor readings.

Your C++ program must:
1. Read the stream line by line.
2. Reshape the wide-format telemetry into a long-format structure internally.
3. Filter the sensor readings: format each float to exactly 3 decimal places (e.g., `12.340`), and check if this string representation exactly matches the `REGEX_PATTERN` (using `std::regex_match`, not partial search).
4. For every matching reading, output a line in the following long format:
`TIMESTAMP,INDEX,FORMATTED_VALUE`
(where `INDEX` is the 0-based index of the reading in that row).

*Example Input:*
`1630000000 ^1[0-9]\.000$ 3 12.000 9.999 15.000`
*Example Output:*
`1630000000,0,12.000`
`1630000000,2,15.000`

**Step 3: Pipeline Orchestration**
Construct a bash pipeline that extracts the telemetry from the video and pipes it directly into your compiled `/home/user/processor`. Save the final output to `/home/user/anomalies.log`.

To ensure your C++ implementation is robust, we have provided an oracle binary at `/app/oracle_processor`. Your compiled C++ program must behave identically to this oracle for any valid telemetry input stream.