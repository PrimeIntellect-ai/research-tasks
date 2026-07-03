You are an AI assistant acting as a storage administrator. We use a proprietary, stripped binary log compression and rotation utility located at `/app/legacy_rotator`. Unfortunately, this utility has bugs. When run on certain log directories, it enters infinite loops due to symbolic link cycles, reads out-of-bounds due to symlinks escaping the log directory, or crashes due to memory exhaustion when encountering excessively long multi-line log records.

Your task is to write a C program that acts as a pre-flight validator (a detector) to classify whether a log directory is safe to process with the legacy rotator. 

You are provided with two corpora of log directories:
- `/app/corpus/clean/`: Contains subdirectories (`case_01`, `case_02`, etc.) that are safe.
- `/app/corpus/evil/`: Contains subdirectories that cause the legacy rotator to crash or hang.

Your C program must be saved as `/home/user/detector.c` and compiled to `/home/user/detector`. 
It must accept exactly one command-line argument: the absolute path to a directory to scan.
It must return exit code `0` if the directory is SAFE (clean), and exit code `1` if it is UNSAFE (evil).

To determine if a directory is UNSAFE, your program must recursively traverse the directory and check for the following conditions. If ANY condition is met, the directory is UNSAFE:
1. **Malicious or Broken Symlinks**: Any symbolic link that resolves to a path outside the target base directory being scanned, or any symbolic link that creates a resolution loop.
2. **Hard Link Count**: Any regular file that has a hard link count greater than 1 (the rotator utility corrupts shared inodes during in-place compression).
3. **Malformed Log Records**: Regular files contain text logs. A log record begins with a timestamp of the exact format `[YYYY-MM-DD HH:MM:SS] ` at the start of a line. A single record spans multiple lines until the next timestamp or EOF. If any single log record exceeds 50 lines (i.e., the timestamp line plus >49 continuation lines), the file is malformed.
4. **Binary Data**: Any regular file that contains a NULL byte (`\0`).

Ensure your implementation in C is efficient and correctly handles large directory structures and large files. You can use standard POSIX C libraries (`dirent.h`, `sys/stat.h`, `unistd.h`, etc.). You must compile your program successfully before finishing the task.

Constraints:
- Do not modify or delete any files in the corpora.
- The `legacy_rotator` binary is provided as a black-box fixture for your reference; you may analyze it if you wish, but your solution purely depends on implementing the above rules correctly in `detector.c`.