You are an AI assistant helping a climate researcher organize and recover a messy archive of custom sensor datasets.

The researcher has a tarball located at `/home/user/raw_data.tar.gz`. When extracted, it will contain a set of file pairs named `rec_001.dat` / `rec_001.txt`, `rec_002.dat` / `rec_002.txt`, etc. 
The `.txt` files contain unstructured researcher notes. 
The `.dat` files contain binary sensor readings saved in a proprietary format.

Your task is to write a C program to parse the binary data, convert it to a standard CSV format, and perform a bulk renaming of the dataset based on the internal binary metadata, finally packaging everything into a clean archive.

Here are the details of the proprietary `.dat` binary format:
- **Bytes 0-3**: Magic sequence `SNSR` (ASCII)
- **Bytes 4-7**: Sensor ID (32-bit unsigned integer, little-endian)
- **Bytes 8-11**: Timestamp (32-bit unsigned integer representing Unix epoch, little-endian)
- **Bytes 12-51**: Sensor Readings (Exactly 10 32-bit IEEE 754 floating-point numbers, little-endian)

Perform the following steps:
1. Extract `/home/user/raw_data.tar.gz` to a temporary workspace.
2. Write a C program at `/home/user/process.c` (and compile it) that can parse the `.dat` files.
3. Create an output directory `/home/user/clean_data/`.
4. Process each `.dat`/`.txt` pair using your C program and bash:
   - Extract the Sensor ID and Timestamp from the `.dat` file.
   - Convert the 10 floating-point readings into a single comma-separated line (e.g., `1.2345,2.3456,...`) formatting each float to exactly 4 decimal places.
   - Save this CSV string into a new file named `/home/user/clean_data/sensor_{ID}_{TIMESTAMP}.csv` (where `{ID}` and `{TIMESTAMP}` are the integer values extracted from the header).
   - Copy the corresponding `rec_XXX.txt` file to `/home/user/clean_data/sensor_{ID}_{TIMESTAMP}.txt`.
5. Generate a log file at `/home/user/conversion.log`. For every file pair processed, append a line in the exact format: `rec_XXX -> sensor_{ID}_{TIMESTAMP}` (sort this file alphabetically by `rec_XXX`).
6. Finally, archive the `/home/user/clean_data/` directory into a gzip-compressed tarball at `/home/user/clean_dataset.tar.gz` (so that extracting it yields the `clean_data` directory and its contents).

Ensure you rely on standard C libraries (`stdio.h`, `stdint.h`, `stdlib.h`, etc.) and GCC is available for compiling your code.