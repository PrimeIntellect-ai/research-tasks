You are an automation specialist building a log analysis workflow. A legacy system generates performance logs in UTF-16LE encoding, and you need to extract and analyze specific error signatures from it.

Your task is to write a C program that processes this file, and then use shell utilities to analyze the output.

Step 1: Write a C program at `/home/user/extract.c` that does the following:
- Reads a UTF-16LE encoded file (from standard input).
- Converts the text to ASCII/UTF-8 (you can assume the relevant characters we care about are all within the ASCII range, so simply handling the UTF-16LE null bytes appropriately is acceptable).
- Uses standard POSIX regex (`<regex.h>`) to find and extract session identifiers. The pattern you must match is `SessionID: ([a-f0-9]{8})`.
- Prints ONLY the 8-character extracted session ID to standard output, one per line.
- Compile this program to an executable at `/home/user/extract` (e.g., using `gcc -O2`).

Step 2: Apply the program and aggregate the results.
- The input log file is located at `/home/user/system.log`.
- Feed this log file to your compiled C program.
- Pipe the output of your C program into standard shell utilities to sort and group the session IDs by frequency.
- Find the top 3 most frequently occurring session IDs.
- Save these top 3 session IDs (JUST the 8-character IDs, one per line, ordered from most frequent to least frequent) to `/home/user/top_sessions.txt`.

Example of the final `/home/user/top_sessions.txt` format:
a1b2c3d4
e5f6g7h8
9i0j1k2l

Do not include counts or leading/trailing whitespace in the final text file.