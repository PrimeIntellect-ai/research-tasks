As a data scientist, I need a high-performance C program to stream-clean a large dataset containing sensitive user information and raw metrics. I've been given a snippet of a document as an image (`/app/rules.png`) that contains the specific mathematical transformations and masking rules our compliance team requires.

Your task:
1. Extract the data mapping rules from the image located at `/app/rules.png`. You can use `tesseract` to read it.
2. Write a C program at `/home/user/cleaner.c` that reads a CSV stream from `stdin` and writes the cleaned CSV to `stdout`.
3. The input CSV will have no header and four columns: `timestamp,user_id,email,value` 
   - `timestamp`: Unix epoch time (integer)
   - `user_id`: Integer
   - `email`: String
   - `value`: Float
4. Only process lines where the `email` ends with exactly `.edu` or `.com`. Skip all other lines.
5. Skip any malformed lines (e.g., missing columns or extra columns).
6. Transform the valid lines according to the four rules found in the image and output them in the format: `bucket,uid,masked_email,val`.
7. Compile your program to an executable at `/home/user/cleaner`. Ensure it is executable.

The program must process data line-by-line (streaming) to handle arbitrarily large files without running out of memory. Ensure precise floating-point formatting as specified in the rules, and exact matching for the email domain filtering.