You are tasked with building a data processing pipeline in C that cleans and anonymizes a telemetry CSV stream.

First, analyze the video artifact located at `/app/telemetry_feed.mp4`. You must extract the exact total number of frames in this video. This frame count will be used as a constant `MAX_RECORDS` in your C program.

Next, write a C program that reads a CSV dataset from standard input (`stdin`) and writes the cleaned CSV to standard output (`stdout`). 

The input CSV has the following structure:
`Timestamp,DeviceID,IPAddress,EventLog`

Your C program must implement the following rules:
1. **Header**: The first line is always the header. It must be printed exactly as received.
2. **Newline Dropping**: The `EventLog` field may be enclosed in double quotes (`"`) and contain embedded newline characters (`\n`). If a row contains an embedded newline, you must silently drop the entire row (do not print it, and it does not count towards `MAX_RECORDS`).
3. **Data Masking**: For the `IPAddress` field, replace the last octet (everything after the last dot `.`) with `XXX`. For example, `192.168.1.105` becomes `192.168.1.XXX`. If there is no dot in the IP address, leave it unchanged.
4. **Deduplication**: You must keep track of `DeviceID`s. If a row has a `DeviceID` that has already been successfully printed, drop the duplicate row.
5. **Termination**: The program should stop reading and exit immediately after it has successfully printed `MAX_RECORDS` data rows (excluding the header), or when it reaches EOF.

Assumptions:
- Maximum row length is 1024 characters.
- Maximum length of a `DeviceID` is 64 characters.
- Columns are separated by commas. Only the `EventLog` column may contain commas or newlines (which will be enclosed in double quotes).
- The input is well-formed CSV (quotes are properly matched).

Compile your C program to `/home/user/cleaner`. Your solution will be tested against a hidden reference oracle using randomized input streams (fuzz equivalence verification). Ensure your program behaves identically to the rules specified.