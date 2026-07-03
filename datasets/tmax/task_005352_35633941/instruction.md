You are a DevOps engineer tasked with debugging a critical log processing pipeline. 

We have an old bash script located at `/app/process_logs.sh` that takes a log file as an argument and decodes it. However, the script has a few critical issues:
1. **Infinite Loop / Loop Termination Bug:** When it encounters heavily corrupted log lines (where the Base64 padding is completely missing or the encoding is truncated), it gets stuck in an infinite loop trying to fix the padding, completely halting our monitoring pipeline.
2. **Missing Configuration:** A crucial severity prefix was lost during a recent migration. We only have a screenshot of the old configuration file containing this 4-letter prefix at `/app/prefix_config.png`. You must extract this text (using OCR tools like `tesseract`, which is installed) and use it to replace the `"UNKNOWN"` placeholder in the script.
3. **Encoding & Corrupted Input Handling Issues:** The logs are double-encoded. The raw log lines are Base64 encoded. Once decoded, they yield a hexadecimal string, which must then be converted to raw ASCII text. Corrupted lines contain non-Base64 characters that must be stripped first.

Your task is to fix the script and save the working version to `/home/user/parser.sh`.

### Parsing Rules for `/home/user/parser.sh`:
For every line in the input file passed as the first argument (`$1`):
1. **Clean:** Remove any character that is NOT a valid Base64 character (`A-Z`, `a-z`, `0-9`, `+`, `/`, `=`).
2. **Decode Base64 & Fix Padding:** Attempt to decode the cleaned Base64 string. If decoding fails due to missing padding, append `=` characters one at a time and retry. **CRITICAL FIX:** You must prevent the infinite loop. If appending up to two `=` characters still doesn't result in a valid decode, or if the cleaned string is empty, you must stop trying and exactly output: `CORRUPT_LOG` (followed by a newline).
3. **Decode Hex:** If the Base64 decode succeeds, the resulting string is a continuous hex string (e.g., `48656c6c6f`). Convert this hex string into standard ASCII text. If the hex conversion yields nothing or fails, output `CORRUPT_LOG`.
4. **Format Output:** Prepend the text with the 4-letter prefix extracted from `/app/prefix_config.png` followed by a colon and a space. 
   Example format: `CRIT: Hello` (assuming the extracted prefix was CRIT).

The system will verify your script by comparing its output against a compiled reference oracle using a fuzzer that generates thousands of random, corrupted, and valid log lines. Your script must process the files identically to the oracle, byte-for-byte.

**Execution:**
Your script will be invoked as: `bash /home/user/parser.sh <input_file>`