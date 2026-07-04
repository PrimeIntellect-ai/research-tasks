You are an automation specialist setting up a fast log processing pipeline. We receive raw, multi-language text logs that contain noise (duplicate entries, trailing whitespaces) and we need to detect sudden changepoints in the log message lengths. Because performance is critical, you must write a C program to perform this filter and detection.

Write a C program at `/home/user/detector.c` and compile it to `/home/user/detector`. 

Your program must read a text file provided as its first command-line argument (e.g., `./detector /home/user/input.txt`) and process it line by line according to the following rules:

1. **Cleaning**: For each line, strip all leading and trailing standard ASCII whitespace characters (spaces, tabs, `\r`, `\n`).
2. **Empty Lines**: If a line becomes empty after stripping, ignore it completely (it does not count towards history and its original line number is just skipped).
3. **Consecutive Deduplication**: If the stripped line is exactly identical to the *most recently accepted* stripped line, ignore it. 
4. **UTF-8 Length**: For each accepted line, calculate its length $L$ in **UTF-8 codepoints** (not bytes!). You can assume the input is well-formed UTF-8.
5. **Changepoint Detection**: Keep track of the UTF-8 codepoint lengths of the last 3 *accepted* lines. If an accepted line has a length $L$ that is strictly greater than twice the integer floor average of the previous 3 accepted line lengths, flag it as an anomaly.
   * *Formula*: `L > 2 * ((L_1 + L_2 + L_3) / 3)` (using integer division).
   * Note: Anomaly detection can only trigger if there are at least 3 previous accepted lines in the history.
6. **Output**: For every anomaly detected, append a line to `/home/user/anomalies.txt` in the exact format:
   `Line {N}: {L} codepoints`
   Where `{N}` is the 1-based line number from the *original* input file, and `{L}` is the calculated UTF-8 codepoint length.

Example of logic:
- Original Line 1: `  Hello ` (Accepted, length 5)
- Original Line 2: `Hello\n` (Skipped, duplicate of stripped "Hello")
- Original Line 3: `Bonjour` (Accepted, length 7)
- Original Line 4: `Hola` (Accepted, length 4)
- Original Line 5: `你好，世界` (Accepted, length 5. Previous lengths: 5, 7, 4. Average=5. 5 is not > 10. No anomaly.)
- Original Line 6: `A very long message exceeding thresholds` (Accepted, length 38. Previous lengths: 7, 4, 5. Average=5. 38 > 10. Anomaly triggered!) -> Output: `Line 6: 38 codepoints`

You will test your program against `/home/user/input.txt`. Be sure to create `/home/user/anomalies.txt` with your results.