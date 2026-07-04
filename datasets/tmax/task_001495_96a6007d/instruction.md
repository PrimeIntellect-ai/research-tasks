You are acting as a log analyst investigating patterns in system events. We have a set of raw log files, but before we can analyze them, we need to clean the messages, remove duplicates, and compute some rolling statistics. 

Unfortunately, the configuration file was lost, but a screenshot of the settings was saved. You will find an image at `/app/window_size.png`. Extract the integer value from this image—it represents the "window size" (`W`) for our rolling statistics computation. (You can use `tesseract` for OCR).

Your task is to write a C++ program that reads log events from standard input, processes them, and prints the results to standard output. Save your source code at `/home/user/process_logs.cpp` and compile it to `/home/user/process_logs`.

Input Format:
The input consists of multiple lines. Each line represents a log event and contains an integer `ID` followed by a space, and then the raw `MESSAGE` payload.
Example: `142 Warning: Disk space is running low!!   Please check.`

Processing Rules:
1. **Tokenization & Normalization**: 
   - Separate the `ID` from the `MESSAGE`.
   - Normalize the `MESSAGE` by:
     - Converting all characters to lowercase.
     - Removing any character that is not alphanumeric (a-z, 0-9) or a space.
     - Collapsing consecutive spaces into a single space.
     - Trimming leading and trailing spaces from the normalized message.
2. **Deduplication**:
   - If the normalized `MESSAGE` is exactly the same as the normalized `MESSAGE` of the immediately preceding valid (non-skipped) log event, **skip** this event entirely. Do not output anything, and do not include it in the rolling statistics.
3. **Rolling Statistics**:
   - Maintain a rolling average of the character length of the normalized messages.
   - The average is computed over the last `W` non-skipped messages (where `W` is the integer you extracted from the image).
   - If fewer than `W` non-skipped messages have been processed so far, compute the average over all non-skipped messages processed up to that point.
   - Use integer division (truncate to integer) for the average.

Output Format:
For each non-skipped event, print a single line to standard output containing:
`[ID] [NORMALIZED_MESSAGE] [ROLLING_AVG]`
(Items separated by a single space).

Example Output:
`142 warning disk space is running low please check 42`

Ensure your C++ program is highly efficient and accurately implements the rules, as it will be rigorously tested against a large number of fuzzed inputs.