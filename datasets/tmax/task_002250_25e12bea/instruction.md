As an automation specialist, you are building a lightweight, high-performance filter to monitor numerical data streams. You need to write a C program that deduplicates the stream in real-time, calculates a rolling average, and detects anomalies.

Create a C program at `/home/user/analyze.c` and compile it to `/home/user/analyze` (use standard `gcc` with no external libraries). 

The program must read a stream of newline-separated integers from standard input (`stdin`) and apply the following logic:
1. **Global Deduplication:** Keep track of every integer seen so far. If an integer has *ever* appeared earlier in the stream, completely ignore it. You should use an efficient data structure (like a basic hash set or a sufficiently large array if you map the values) to track seen values.
2. **Rolling Statistics:** Maintain a sliding window of the last **4** *unique* integers. 
3. **Anomaly Detection:** Wait until you have at least 4 unique integers in your window. From the 5th unique integer onwards, calculate the floating-point average of the *previous 4* unique integers. If the new unique integer is strictly greater than `(average + 10.0)`, flag it.
4. **State Update:** Add the new unique integer (whether anomalous or not) to the sliding window, replacing the oldest value.
5. **Output:** For every detected anomaly, print exactly `Anomaly: %d\n` to standard output.

Once compiled, run your program using the existing data file `/home/user/stream.txt` as input, and redirect the output to `/home/user/anomalies.txt`.

Example conceptual flow:
If the stream is `10, 12, 11, 10, 13, 15`:
- `10, 12, 11` are unique. Window: `[10, 12, 11]`
- `10` is a duplicate (ignored).
- `13` is unique. Window: `[10, 12, 11, 13]`. Average of window is `11.5`.
- `15` is unique. Is it > `(11.5 + 10.0)`? No. New Window: `[12, 11, 13, 15]`.