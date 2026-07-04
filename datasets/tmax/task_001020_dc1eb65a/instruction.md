You are assisting a backup administrator in filtering a stream of corrupted archive files. We need a robust Bash script to stream archive records, extract their headers, and verify their integrity based on a specific magic signature.

An image of the physical tape label is located at `/app/tape_label.png`. You must read this image to find the "MAGIC" signature required for valid backups (it will be clearly labeled). 

Write a script at `/home/user/filter_backup.sh` that does the following:
1. Reads continuously from standard input (`stdin`) line by line.
2. Expects each line to be formatted exactly as: `MAGIC|SIZE|DATA` (where `MAGIC` is a string, `SIZE` is an integer representing the expected character count of `DATA`, and `DATA` is the remaining string on that line, which may contain spaces or special characters).
3. Extracts the header information to perform two archive integrity checks:
   a. The `MAGIC` field must exactly match the magic signature extracted from `/app/tape_label.png`.
   b. The `SIZE` field must exactly match the actual character length of the `DATA` field.
4. For each line:
   - If both integrity checks pass, output to `stdout`: `OK: <DATA>` (replace `<DATA>` with the actual data payload).
   - If either check fails, or if the line does not match the expected `MAGIC|SIZE|DATA` structure, output to `stdout`: `ERR: <ENTIRE_RAW_LINE>`

Requirements:
- Your script must be written entirely in Bash (using built-ins and standard coreutils like `awk`, `grep`, `sed`, `wc`, etc. is permitted).
- Do not hardcode the expected magic signature if it changes, though for this task you can just extract it and use it directly.
- The script must be executable (`chmod +x`).
- Handle streaming input efficiently (do not buffer the entire input before processing).

Example:
If the required magic signature was `TEST` and the script received:
`TEST|4|abcd`
`TEST|5|abcd`
`BAD|4|1234`
`TEST|6|123456`

The output should be:
`OK: abcd`
`ERR: TEST|5|abcd`
`ERR: BAD|4|1234`
`OK: 123456`