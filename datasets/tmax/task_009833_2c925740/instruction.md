You are an AI assistant helping a researcher organize and clean up some raw dataset files.

The researcher has provided a nested archive located at `/home/user/dataset_archive.tar.gz`. This gzip archive contains multiple uncompressed tar archives (`archive1.tar`, `archive2.tar`, etc.), which in turn contain multiple text files with `.txt` extensions (e.g., `sensor1.txt`). These text files contain one integer per line representing sensor readings.

Your task is to:
1. Extract all the `.txt` files from the nested archives.
2. Write a C program `/home/user/filter_dataset.c` that parses the configuration file `/home/user/config.ini`. This configuration file contains a single line in the format `THRESHOLD=X`, where `X` is an integer. 
3. The C program must read integers from standard input (`stdin`) line by line, and write only the integers that are strictly greater than the threshold `X` to standard output (`stdout`), each followed by a newline.
4. Compile your C program to `/home/user/filter_dataset`.
5. For each extracted `.txt` file, use your compiled C program to filter its contents by piping the file into the program via standard input and redirecting the standard output to a new file in the `/home/user/filtered/` directory. The filtered file must have the exact same filename as the original (e.g., `/home/user/filtered/sensor1.txt`).
6. Finally, generate a SHA-256 checksum manifest for all the files inside `/home/user/filtered/`. The manifest must be saved to `/home/user/manifest.txt` and formatted exactly like the output of the `sha256sum` command (e.g., `<checksum>  <filename>`), containing only the base filename (no directory paths). Sort the lines in the manifest alphabetically by filename.

Ensure your C program is robust and cleanly handles the standard streams. Do not modify the original archives.