You are acting as a storage administrator managing disk space. We have a set of old, compressed log files from legacy systems that are taking up too much space. They are filled with verbose debug messages and use an outdated character encoding. 

Your objective is to process these logs to remove the debug messages, convert their encoding to UTF-8, and save the cleaned logs with a new naming convention, along with a checksum manifest.

Specifically, perform the following steps:
1. Write a C program at `/home/user/filter.c` that reads text line-by-line from standard input. It should silently discard any line that begins exactly with the string `[DEBUG] ` and print all other lines to standard output.
2. Compile this program to an executable at `/home/user/filter`.
3. Process all `.log.gz` files located in the directory `/home/user/old_logs/`. These files are compressed with gzip and their plain-text contents are encoded in `ISO-8859-1`.
4. For each file, you must:
   - Decompress the stream.
   - Convert the text from `ISO-8859-1` to `UTF-8`.
   - Filter out the debug lines using your compiled `/home/user/filter` C program.
   - Recompress the stream using gzip.
   - Save the resulting file in `/home/user/new_logs/` (you will need to create this directory). The new filename should be the original filename with `.filtered` inserted before `.log.gz`. For example, `app_server.log.gz` becomes `app_server.filtered.log.gz`.
5. Finally, generate a SHA256 manifest of all the newly created files in `/home/user/new_logs/` and save it to `/home/user/manifest.sha256`. The manifest should be in the standard `sha256sum` format, and the file paths listed in the manifest should be just the basenames of the files (e.g., `app_server.filtered.log.gz`, not the full path).

Ensure your C program handles lines up to at least 1024 characters properly. You may use standard bash utilities (like `zcat`, `iconv`, `gzip`, `sha256sum`) alongside your C program to complete the pipeline.