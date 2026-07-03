You are an AI assistant helping a climate researcher organize a fragmented dataset. 

The researcher has received a compressed dataset archive located at `/home/user/raw_dataset.tar.gz`. Due to errors in the data collection pipeline, the dataset was split into chunks, and some of the chunks were saved using different character encodings.

Your task is to write a C program that unifies, converts, and filters this data, and then package the results.

Here is the exact step-by-step pipeline you need to implement:

1. **Extract the Archive**: Extract `/home/user/raw_dataset.tar.gz`. It contains a manifest file `manifest.csv` and several chunk files (`data_part1.csv`, `data_part2.csv`, etc.).

2. **Write a C Program**: Create a C program at `/home/user/process_data.c` that does the following:
   - Reads `manifest.csv`. Each line in the manifest contains a filename and its corresponding character encoding, separated by a comma (e.g., `data_part1.csv,UTF-8`).
   - Merges the data from all the chunk files in the order they appear in the manifest.
   - During merging, converts the text of each chunk from its original encoding (as specified in the manifest) into `UTF-8`. You should use the POSIX `iconv` API (`<iconv.h>`) for this.
   - Parses the merged CSV data. The CSV has the following columns: `ID,Timestamp,Sensor,Value,Notes`. (Note: Only the first chunk contains the header row; subsequent chunks only contain data rows).
   - Filters the data to only include rows where the `Sensor` is exactly `"TEMP_01"` AND the `Value` is strictly greater than `25.0`.
   - Writes the header row and the filtered data rows to a new file called `/home/user/filtered_dataset.csv`.

3. **Compile and Run**: Compile your C program to an executable named `/home/user/process_data` (you may use GCC and link any standard libraries necessary). Run the executable to produce `/home/user/filtered_dataset.csv`.

4. **Summarize**: Create a file named `/home/user/summary.txt` that contains exactly the following text, replacing `<N>` with the number of data rows (excluding the header) that passed the filter:
   `Filtered rows: <N>`

5. **Package**: Create a gzip-compressed tar archive at `/home/user/processed_dataset.tar.gz` that contains `filtered_dataset.csv` and `summary.txt` at the root of the archive (do not include the `/home/user/` directory structure inside the tarball).

Ensure all resulting files have standard read permissions so they can be verified.