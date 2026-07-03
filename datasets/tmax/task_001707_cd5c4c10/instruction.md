You are an IT support technician working on Ticket #8819. An internal database ingestion service recently crashed, leaving behind a corrupted Write-Ahead Log (WAL), a memory dump, and a screenshot of the exact error message reported by the user's terminal.

Your goal is to write a data recovery script that can parse corrupted WAL files and extract the valid transactions, functionally replacing the crashed system.

Here are your steps:
1. Examine the user's error screenshot located at `/app/error_screenshot.png` (you can use tools like `tesseract` to read it). You will need to extract the failing "MODULE_ID" from this image.
2. We have captured a memory core dump of the crashed process at `/app/crash.dmp`. Analyze this memory dump to find the configuration string associated with the failing MODULE_ID you found in step 1. The memory dump contains a specific configuration entry that dictates the exact regular expression format of valid transaction records for this specific module.
3. Using the regex format discovered in step 2, write a Bash script at `/home/user/wal_recover.sh`. 
   - The script must read a stream of raw, potentially corrupted binary/text data from standard input (`stdin`).
   - It must extract and print only the transaction records that perfectly match the regex/format intended for the crashed module.
   - Each extracted record should be printed on a new line.
   - The script must be robust against null bytes and binary garbage.
   - Use only standard Bash tools (grep, sed, awk, tr, etc.).

Your final script (`/home/user/wal_recover.sh`) will be tested exhaustively against a hidden reference implementation using randomized corrupted inputs to ensure bit-exact equivalence in the recovery process. Ensure the script is executable.