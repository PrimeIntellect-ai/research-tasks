You are an IT support technician. We've received a ticket that our internal log sanitizer tool is crashing under load, dropping valid log files, and failing to block malicious log formats. 

A vendored version of the tool's source code is located at `/app/log_filter-1.0.0`. 
The tool is designed to read a directory of log files and copy the valid ones to an output directory using a multithreaded worker pool. 

However, there are three known issues:
1. **Concurrency Bug:** A race condition in the worker pool (`worker.c`) causes occasional crashes and dropped files.
2. **Format Parsing Edge-Case:** The parser (`parser.c`) fails to properly detect and reject malicious logs containing non-printable characters (like embedded nulls or control characters outside of valid whitespace) and excessively long lines (over 1024 characters).
3. **Missing Assertion Validation:** A critical `assert()` in `main.c` fails because a global initialization flag is not being set properly.

Your task is to:
1. Debug and fix the source code in `/app/log_filter-1.0.0`.
2. Compile the fixed program.
3. Place the final compiled executable at `/home/user/log_filter`.

The compiled executable will be tested against two corpora of log files:
- **Clean Corpus:** Standard, valid log files. The tool MUST copy 100% of these files to the output directory unchanged.
- **Evil Corpus:** Malicious log files containing invalid characters or overflowing lines. The tool MUST reject (not copy) 100% of these files.

The program's expected signature is:
`/home/user/log_filter <input_directory> <output_directory>`