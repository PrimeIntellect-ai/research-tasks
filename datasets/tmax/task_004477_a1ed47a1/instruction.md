I'm organizing some old project files and I came across a legacy application log dump located at `/home/user/legacy_project_logs.tar.gz`. 

This is a nested archive. Inside the `.tar.gz` file is a `.zip` archive, and inside that `.zip` archive is a single text file named `application.log`. This log file is encoded in `UTF-16LE`.

I need you to write and run a Python script to extract specific error records from this log and save them to a new file.

Here are the requirements:
1. Extract the `application.log` from the nested archives.
2. Write a Python script to parse `application.log`. Because these log files are typically massive in our production environments, your Python script **must** process the file using memory-mapped I/O (`mmap`) or line-by-line streaming. Do not read the entire file into memory at once.
3. The log file contains multi-line records. Every new log record starts with a bracketed log level, like `[INFO]`, `[WARN]`, or `[ERROR]`. Any subsequent lines that do not start with `[` belong to the preceding log record (e.g., stack traces).
4. Extract **only** the complete `[ERROR]` records (including their multi-line details).
5. Convert these extracted error records to standard `UTF-8` encoding.
6. Write the extracted `UTF-8` error records to exactly `/home/user/extracted_errors.log`. Maintain the exact original line breaks and indentation for the error records.

Please complete this task so I can review `/home/user/extracted_errors.log`.