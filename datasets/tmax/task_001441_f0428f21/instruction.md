You are a data analyst tasked with cleaning up a poorly formatted CSV file using C. 

The file is located at `/home/user/data.csv` and contains three columns: `ID`, `Category`, and `Text`.
Due to a bug in a previous data export pipeline, the `Text` column (which is enclosed in double quotes) contains unescaped JSON-style unicode sequences (like `\u20ac` for the Euro symbol) and erratic whitespace (newlines, tabs, and multiple spaces).

Your objective is to write a C program at `/home/user/parser.c` that reads `/home/user/data.csv` and writes a cleaned, normalized Tab-Separated Values (TSV) file to `/home/user/output.tsv`.

Program requirements:
1. **Multi-format handling**: Read the CSV input and convert it to TSV output. The output should not contain any quotes around the text. The three columns must be separated by a single tab character (`\t`).
2. **Character Encoding**: Detect any `\uXXXX` sequences (where `X` is a hex digit, case-insensitive) in the `Text` column and decode them into their proper UTF-8 byte representation.
3. **Tokenization and Normalization**: Normalize all whitespace inside the `Text` column. Any sequence of whitespace characters (spaces, tabs, newlines) should be collapsed into a single space character (` `). Leading and trailing whitespace within the text field should be removed.

Format of `/home/user/data.csv`:
- `ID`: Integer (no quotes)
- `Category`: String (no quotes, no commas)
- `Text`: String enclosed in double quotes (`"`). It will not contain escaped internal quotes.

Compile your program using: `gcc -O3 /home/user/parser.c -o /home/user/parser`
Then run it so that it reads the CSV and produces `/home/user/output.tsv`.

Ensure your C program is robust and correctly handles the UTF-8 bitwise conversions for the Unicode codepoints present.