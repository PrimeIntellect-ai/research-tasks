I am a researcher working with a massive dataset of system logs, and I need your help to extract and clean the data. 

We have a custom C-based extraction tool located at `/app/log_extractor-1.0.2/` that was built to decompress our specific binary archive format. Unfortunately, the developer who wrote it left some broken build configuration behind. When I try to run `make` in that directory, the compilation fails.

Here is what I need you to do:
1. Fix the build configuration (Makefile) in `/app/log_extractor-1.0.2/` so that the `extractor` binary successfully compiles.
2. Use the compiled `extractor` tool to decompress the archive `/app/raw_data.bin` and save the output to `/home/user/logs.txt`. The tool takes two arguments: the input file and the output file.
3. The extracted file `/home/user/logs.txt` contains multi-line log records. Each record begins with `RECORD_START <ID>` and ends with `RECORD_END`. Between these markers, there are lines specifying `Value: <number>` and `Status: <string>`.
4. Due to a logging system error, some of these records are corrupted and contain binary junk (non-printable characters). A record is considered corrupted if it contains ANY byte that is not a standard printable ASCII character (bytes 32 through 126 inclusive) or standard whitespace (tab `\t` (9), newline `\n` (10), carriage return `\r` (13)).
5. Write a script to parse `/home/user/logs.txt`, completely discard any corrupted records, and extract the `ID`, `Value`, and `Status` from the valid records.
6. Output the cleaned data as a CSV file to `/home/user/cleaned_data.csv` with the exact header: `ID,Value,Status`.

You can use Bash, Python, or any standard Linux tools available. Our evaluation suite will compute the F1 score of the extracted IDs in your CSV against our ground-truth list of valid IDs to ensure you have correctly filtered out the corruption.