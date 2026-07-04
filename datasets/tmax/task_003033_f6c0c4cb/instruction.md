You are a localization engineer. We have been using a legacy proprietary tool located at `/app/loc_filter` to process translation CSV dumps. The tool reads text from standard input, performs data masking (anonymizing emails), calculates rolling similarity metrics (Levenshtein distance between consecutive valid translations), and outputs structured text to standard output. 

Unfortunately, the original source code for this tool is lost, and we recently discovered it has a bug where it silently mishandles CSV rows containing embedded newlines (it simply reads line-by-line and breaks). Because our downstream systems have come to rely on its *exact* output format and quirks, we need a drop-in replacement written in C++ that perfectly mimics its behavior, bugs and all.

Your task:
1. Reverse-engineer the behavior of the stripped binary `/app/loc_filter` by probing it with various inputs. Pay attention to how it parses lines, what regex/pattern it uses to identify and mask emails, how it calculates the distance metric between consecutive rows, and how it formats the output.
2. Write a C++ program in `/home/user/solution.cpp` that implements this exact logic.
3. Compile your program to `/home/user/solution` (e.g., `g++ -O3 /home/user/solution.cpp -o /home/user/solution`).

Your executable must read from standard input until EOF and write to standard output. An automated verification system will fuzz both `/app/loc_filter` and your `/home/user/solution` with thousands of random inputs to ensure their outputs are bit-for-bit identical.