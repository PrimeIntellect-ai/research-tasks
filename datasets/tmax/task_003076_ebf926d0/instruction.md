You are a backup administrator responsible for archiving system logs. Before archiving, we need to ensure that no compromised or malicious logs are included in our secure backups. 

You must build a C++ CLI tool, compiled to `/home/user/log_checker`, that determines whether a given log file is safe to archive ("clean") or contains malicious payload signatures ("evil").

**Part 1: Fix the Vendored Package**
We rely on a custom C++ library called `BackupUtils-1.2.0`, whose source is vendored at `/app/vendored/BackupUtils-1.2.0`.
- The library provides useful file I/O and character encoding conversion utilities (e.g., converting UTF-16LE or ISO-8859-1 to UTF-8).
- The package currently fails to compile due to a configuration or code perturbation introduced during an incomplete migration.
- Your first task is to identify the issue in the package, fix it, compile it, and generate the static library (`libbackuputils.a`). 

**Part 2: Implement the Classifier**
Write a C++ program at `/home/user/log_checker.cpp` and compile it to `/home/user/log_checker`. 
- You must link against the fixed `BackupUtils` library.
- The program must accept a single command-line argument: the path to a log file.
- `Usage: /home/user/log_checker <path_to_log_file>`
- The tool must read the file, detect its encoding (logs may be in UTF-8, UTF-16LE, or ISO-8859-1), and convert the text to UTF-8 for analysis. (You may use functions provided by `BackupUtils` or standard C++ combined with system tools/headers).
- **Classification Rule:** A file is "evil" if, after being converted to a valid UTF-8 string, it contains the exact string `"RANSOMWARE_PAYLOAD"` (case-insensitive). Otherwise, it is "clean".
- If the file is **clean**, the program must print `CLEAN` to standard output and exit with status code `0`.
- If the file is **evil**, the program must print `EVIL` to standard output and exit with status code `1`.

**Testing and Evaluation**
Your program will be evaluated against a hidden corpus of files. However, you are provided with sample files to test your implementation:
- Clean corpus: `/app/corpora/clean/`
- Evil corpus: `/app/corpora/evil/`

Your binary at `/home/user/log_checker` must achieve 100% accuracy on both the clean and evil corpora (exit 0 for all clean files, exit 1 for all evil files).