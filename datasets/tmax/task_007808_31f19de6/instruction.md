You are managing an artifact repository where binaries are continuously uploaded. You have a snapshot of the repository logs and the uploaded files. Your goal is to curate these files, filter out corrupted uploads, and prepare a final archive and report.

In `/home/user/artifacts/`, there are several binary files.
In `/home/user/repo.log`, there is a multi-line text log of the uploads. Each entry in the log has the following exact format:
```
BEGIN ARTIFACT
File: <filename>
Magic: <8-character hex string>
Desc: <A single-line description encoded in ISO-8859-1>
END ARTIFACT
```

Write a C program at `/home/user/curator.c` (and compile it to `/home/user/curator`) that does the following when run:
1. Parses `/home/user/repo.log`.
2. For each artifact listed, opens the corresponding file in `/home/user/artifacts/` in binary mode.
3. Reads the first 4 bytes of the file and checks if they match the expected `Magic` hex value from the log. For example, if Magic is `DEADBEEF`, the first 4 bytes of the file must be `DE AD BE EF` in that exact order.
4. If the file is missing or the magic bytes do not match, the artifact is considered invalid and should be skipped.
5. If the artifact is valid, the program must append its details to a CSV report at `/home/user/valid_artifacts.csv`. The CSV must have the header `Filename,Magic,Description` on the first line. Subsequent lines should contain the data for valid artifacts.
6. The `Description` field in the CSV must be converted from its original ISO-8859-1 encoding to valid UTF-8.
7. Finally, your program (or a supplementary bash script you write and execute) must create a compressed archive at `/home/user/curated.tar.gz` containing *only* the valid artifact files. The files inside the archive must not include any directory paths (i.e., they should be at the root of the archive).

Requirements:
- Ensure `/home/user/valid_artifacts.csv` uses proper UTF-8 encoding.
- Ensure `/home/user/curated.tar.gz` extracts directly to the valid files without parent directories.
- You may use standard C library functions and standard Linux utilities (via `system()` or bash wrappers) to complete the task.