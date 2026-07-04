You are an operations engineer triaging a critical incident (Ticket #8832) involving our core data processing pipeline. 

We recently migrated our data stream parsing from a slow, legacy C binary to a new Python implementation (`/home/user/parser/fast_parser.py`). However, the new implementation is failing in production.

Here are the details from the incident report:
1. **Crash Loops**: The new script is frequently throwing `RecursionError` and infinite looping on certain nested data streams (which consist of alphanumeric characters and nested parentheses). 
2. **Configuration Loss**: A recent deployment wiped the environment variables. The system dashboard screenshot taken right before the crash was saved to the ticket as `/app/ticket_screenshot.png`. It contains a vital `CRITICAL_OFFSET` integer value that must be hardcoded into the `CONFIG_OFFSET` variable in `fast_parser.py`.
3. **Data Mismatch**: Even when it doesn't crash, the output does not perfectly match the old legacy parser.

Your objectives:
1. **Extract Configuration**: Analyze the image at `/app/ticket_screenshot.png` (using OCR tools like `tesseract` which are available) to find the `CRITICAL_OFFSET` value. Update `CONFIG_OFFSET` in `fast_parser.py` with this exact integer.
2. **Debug and Fix**: Use debugging techniques to trace the recursion errors and logic bugs in `/home/user/parser/fast_parser.py`. Fix the code so it properly parses nested structures without overflowing the stack or getting stuck in infinite loops.
3. **Achieve Parity**: The fixed `fast_parser.py` must read from `stdin` and print to `stdout`. Its output must be exactly bit-for-bit identical to the legacy oracle binary located at `/app/legacy_parser` for any valid or invalid input string.

You can test your implementation locally by piping various test strings containing uppercase letters, numbers, and parentheses into both `/app/legacy_parser` and `python3 /home/user/parser/fast_parser.py` and comparing the results. Use delta debugging to minimize failing test cases if you encounter mismatches.

Ensure your final fixed script remains at `/home/user/parser/fast_parser.py`. An automated fuzzing system will verify your solution by feeding hundreds of random strings to both your script and the oracle.