Hello! I am trying to organize some legacy project logs, but they are a mess. They are split into several compressed chunks and use an outdated text encoding. 

I need you to write and run a Python script at `/home/user/organize.py` that will clean this up for me. 

Here are the details:
1. The input files are located in `/home/user/incoming/`. They are named `chunk_a.gz`, `chunk_b.gz`, and `chunk_c.gz`.
2. These files contain gzip-compressed text data. The underlying text is encoded in `cp1252` (Windows-1252).
3. Your Python script must read these chunks in alphabetical order, decompress them on the fly, and convert the text from `cp1252` to `UTF-8`.
4. As it processes the combined stream, the script should split the output into multiple uncompressed text files, each containing exactly 500 lines (except the last file, which will contain whatever lines are remaining).
5. The output files must be saved in a new directory at `/home/user/organized/`.
6. Name the output files using the pattern `clean_log_000.txt`, `clean_log_001.txt`, `clean_log_002.txt`, and so on.

Please create the `organized` directory in your script, process the files, and leave the resulting `UTF-8` text files in the `organized` directory. Run your script to complete the task.