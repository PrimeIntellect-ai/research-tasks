You are a localization engineer tasked with processing a large batch of translation updates. Our translation vendors delivered the strings in a broken JSON-lines format. Specifically, some lines contain improperly formatted unicode escape sequences (e.g., `\u12Z3` instead of `\u00A9`), which are crashing our downstream systems. 

Your objective is to extract the translation data, apply validation checks to drop corrupted lines, and transform the valid records into a clean CSV file using parallel processing to handle the batch quickly.

**Requirements:**

1.  **Write a C program** at `/home/user/loc_parser.c`:
    *   The program must read text from standard input (stdin) line-by-line.
    *   Use POSIX regex (`<regex.h>`) to parse the JSON-lines. Each line has the format: `{"msgid": "SOME_ID", "msgstr": "SOME_TRANSLATION"}`.
    *   Extract the values of `SOME_ID` and `SOME_TRANSLATION`. Note: The translation string might contain spaces and punctuation.
    *   **Validation Checkpoint:** Validate the `SOME_TRANSLATION` string for unicode escape sequences. A valid sequence is EXACTLY the literal string `\u` followed by exactly 4 hexadecimal digits (e.g., `\u0021`, `\uF8A0`). 
    *   If the translation string contains a `\` followed by `u` but it is NOT followed by exactly 4 hex digits, consider the line corrupted and drop it (do not output anything for that line).
    *   If the line is valid (either no `\u` sequences, or all `\u` sequences are valid 4-hex-digit sequences), output the extracted data to standard output (stdout) as comma-separated values: `SOME_ID,SOME_TRANSLATION`.
    *   Ensure your C program compiles cleanly into an executable at `/home/user/loc_parser`.

2.  **Write a shell script** at `/home/user/process_locales.sh`:
    *   The script should first compile your C program.
    *   Use parallel data processing (e.g., `xargs -P 4` or `parallel`) to run `./loc_parser` on all `.jsonl` files located in the directory `/home/user/locales/`. There are multiple files, and they must be processed concurrently.
    *   The script must collect the standard output of all these parallel executions.
    *   The final output should be written to `/home/user/valid_translations.csv`.
    *   The first line of `/home/user/valid_translations.csv` MUST be the header: `msgid,msgstr`. The subsequent lines should be the valid, parsed data from all files. (The order of the data lines does not matter).

**Constraints:**
*   Do not use external C libraries (like Jansson or cJSON); you must use native string manipulation and POSIX regex (`<regex.h>`) to achieve the extraction and validation.
*   Assume the `msgid` and `msgstr` values themselves do not contain unescaped double-quotes.
*   The system is a standard Linux environment.