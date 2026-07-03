You are tasked with building a data cleaning pipeline for a dataset containing potentially sensitive information. 

First, we received an image containing the list of sensitive keywords that need to be masked, located at `/app/pii_list.png`. You need to extract the text from this image (using OCR tools like `tesseract`) to obtain the list of forbidden words. The words are printed one per line.

Second, you must write a Rust program that acts as a stream processor. The program should be compiled to an executable at `/home/user/cleaner`.

The Rust program must adhere to the following specifications:
1. It accepts exactly one command-line argument: the path to a text file containing the forbidden words (one per line, in the exact order they appeared in the image).
2. It reads lines from `stdin` until EOF.
3. For each line:
   - Decode the line assuming it is URL-encoded (e.g., `%20` becomes space). Assume the decoded text is valid UTF-8.
   - Mask occurrences of the forbidden words. You must perform substring replacement for each forbidden word in the exact order they appear in your dictionary file. Replace each occurrence with `[REDACTED]`. The matching should be case-sensitive.
   - Keep track of the total number of `[REDACTED]` replacements made in the current line.
   - Maintain a rolling sum of the number of replacements made over the last 3 lines (the current line and the up to 2 preceding lines).
   - Output to `stdout` the exact line: the redacted UTF-8 string, followed by a single tab character (`\t`), followed by the rolling sum of replacements. 
   - Terminate each output line with a newline (`\n`).

Example of rolling sum:
Line 1: 2 replacements -> rolling sum = 2
Line 2: 1 replacement -> rolling sum = 3
Line 3: 0 replacements -> rolling sum = 3
Line 4: 5 replacements -> rolling sum = 6 (Line 2 + 3 + 4)

Ensure your program is highly efficient and handles large streams properly (do not load the entire stdin into memory at once). Your final compiled binary must be located at `/home/user/cleaner`.