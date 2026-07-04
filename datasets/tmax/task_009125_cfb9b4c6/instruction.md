You are a data engineer building a high-performance ETL pipeline. You need to write a C program that performs tokenization, aggregation, and template-based text generation on a raw UTF-8 text dump. 

Your task is to write a C program at `/home/user/etl_step.c`, compile it to an executable named `/home/user/etl_step`, and run it to generate a final report.

**Inputs:**
1. `/home/user/corpus.txt`: A UTF-8 encoded text file where each line is a separate document.
2. `/home/user/report.tmpl`: A template file containing placeholders for summary statistics.

**Processing Requirements:**
1. **Tokenization:** Read `/home/user/corpus.txt` line by line. Tokenize the text into words using standard ASCII whitespace characters (space `' '`, tab `'\t'`, and newline `'\n'`) as delimiters.
2. **Unicode Processing:** Calculate the length of each word in terms of **Unicode characters (code points)**, NOT bytes. Since the file is UTF-8 encoded, remember that continuation bytes in UTF-8 start with the bit pattern `10xxxxxx` (i.e., byte values between `0x80` and `0xBF`). 
3. **Aggregation:** Compute the following statistics across the entire file:
   - Total number of lines.
   - Total number of words.
   - The maximum length of a word (in Unicode characters).
4. **Template Generation:** Read `/home/user/report.tmpl` and replace the following exact placeholders with your calculated integer values:
   - `{{LINES}}` -> Total number of lines
   - `{{WORDS}}` -> Total number of words
   - `{{MAX_LEN}}` -> Maximum word length (in Unicode characters)
5. **Output:** Write the resulting text to `/home/user/report.txt`.

**Notes:**
- You may use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, etc.).
- The corpus may contain blank lines. A blank line counts towards the total line count but contributes 0 words.
- Your program should cleanly handle the file reading, writing, and memory management. Run your compiled executable to produce the final `report.txt`.