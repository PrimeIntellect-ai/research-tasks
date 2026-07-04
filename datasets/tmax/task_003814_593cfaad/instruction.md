I need you to help me organize an old project repository that was broken into chunks and scattered across a deep directory structure to bypass some old email attachment size limits. 

The scattered files are located in `/home/user/project_scatter`. The files are binary chunks of a single `tar.gz` archive. Each chunk is named with the pattern `*part<N>.chunk`, where `<N>` is an integer representing its sequential order (e.g., `backup_part1.chunk`, `misc_part2.chunk`, etc.). Note that the prefixes before `_part` vary and should be ignored; only the part number determines the order.

Please write a C++ program at `/home/user/assembler.cpp` and compile it to an executable named `/home/user/assembler`.

When executed, your C++ program must:
1. Recursively traverse `/home/user/project_scatter` to find all files ending in `.chunk`.
2. Determine their correct order based on the `<N>` integer in their filenames.
3. Read these binary chunks and merge them in sequential order (1, 2, 3...) to reconstruct the original archive at `/home/user/reassembled_project.tar.gz`.
4. Verify the integrity of the assembled archive by extracting a file named `manifest.txt` from it to `/home/user/manifest.txt`. (You can use `system()` calls to invoke `tar` if needed).
5. Read `/home/user/manifest.txt` (which contains multiple lines) and create a log file at `/home/user/manifest_summary.txt` containing exactly the contents of the *first line* of the manifest file, followed by a newline.

Your solution must rely on the C++ program to do the traversal, sorting, binary merging, and text extraction logic. Do not just write a bash script for the main logic.