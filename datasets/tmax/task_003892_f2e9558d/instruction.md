You are helping a researcher organize a chunked text dataset. The dataset is located in `/home/user/dataset/`. However, the script that generated the dataset had a bug: it created an infinite symlink loop within the directory (e.g., a symlink pointing back to the directory itself).

The dataset consists of multiple data chunks named `chunk_*.dat`. These chunks contain text encoded in UTF-16LE. 

Your task is to write and compile a C program that safely merges these chunks into a single UTF-8 encoded file. 

Create your C program at `/home/user/merge_dataset.c` and compile it to an executable at `/home/user/merge_dataset`. 

The program must meet the following requirements:
1. Traverse the `/home/user/dataset/` directory and identify all regular files ending in `.dat`. It must explicitly ignore symlinks or directories to avoid falling into the infinite symlink loop.
2. Sort the identified chunk files alphabetically by filename.
3. Read the contents of each valid chunk (which are in UTF-16LE).
4. Convert the text to UTF-8.
5. Append the converted text to an output file located at `/home/user/merged_output.txt`.
6. Concurrency Safety: The researcher plans to run multiple instances of this tool in the future. Therefore, your program MUST acquire an exclusive file lock (`LOCK_EX`) on `merged_output.txt` using `flock()` (from `<sys/file.h>`) before writing each chunk's data, and release the lock (`LOCK_UN`) immediately after writing.

Once your program is written and compiled, run it to generate `/home/user/merged_output.txt`.

Ensure the final `merged_output.txt` contains the correctly ordered, UTF-8 encoded text from all valid chunks.