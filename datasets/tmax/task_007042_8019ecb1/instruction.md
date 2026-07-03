I am a researcher organizing a batch of raw sensor datasets, but they were saved in a custom binary format that my standard data analysis tools can't read. 

I have an archive located at `/home/user/raw_sensors.tar.gz` which contains 5 binary files (named `sensor_1.bin` to `sensor_5.bin`). 

Each binary file contains a sequence of data records. Every record is exactly 8 bytes long and consists of:
1. A 32-bit signed integer (`id`)
2. A 32-bit floating-point number (`value`)
Both are in little-endian byte order.

I need you to perform the following steps to clean and transform this dataset:
1. Extract the binary files.
2. Write a C program at `/home/user/converter.c` (and compile it) that reads these binary records and prints them as comma-separated text (`id,value`), formatting the floating-point value to exactly 2 decimal places.
3. Process all the extracted `.bin` files to produce a single, combined list of records.
4. Filter out any records where the `value` is less than or equal to `0.00`.
5. Sort the remaining records numerically by `id` in ascending order.
6. Save this final sorted list as `/home/user/dataset.csv`.
7. Finally, compress `dataset.csv` into a new gzip-compressed tar archive located at `/home/user/clean_dataset.tar.gz`.

Do not include any header row in the CSV. Your final state must include the compiled C program, the `/home/user/dataset.csv` file, and the `/home/user/clean_dataset.tar.gz` file.