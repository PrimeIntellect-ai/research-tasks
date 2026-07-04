I need you to help me organize a messy project log dump by writing a C++ utility. Our legacy system dumped all project file metadata into a single custom binary file, and I need it parsed, converted, and split into manageable text chunks based on a configuration file.

Here are the specific requirements:

1. Read the configuration file located at `/home/user/chunk_config.ini`. It contains key-value pairs (one per line, separated by `=`). You need to extract two keys:
   - `max_chunk_size`: The maximum size in bytes for any output chunk file.
   - `output_dir`: The directory where chunk files should be saved.

2. Read the binary log dump located at `/home/user/project_dump.bin`. The file consists of a sequence of records. Each record is formatted as:
   - A 4-byte little-endian unsigned integer `N`, representing the length of the string data in bytes.
   - `N` bytes of text encoded in **UTF-16LE**.

3. Your C++ program must:
   - Read each record from the binary dump.
   - Convert the UTF-16LE text payload into **UTF-8**.
   - Write the UTF-8 text to chunk files inside the `output_dir`.
   - The chunk files must be named sequentially: `chunk_001.log`, `chunk_002.log`, `chunk_003.log`, etc.
   - You must write whole records. If adding the next UTF-8 record to the current chunk file would cause its file size to exceed `max_chunk_size`, you must close the current chunk and start a new one. (Assume no single record is larger than `max_chunk_size`).

4. After processing all records, generate an index file at `/home/user/chunks/index.txt`.
   Each line of `index.txt` should contain the chunk filename and the number of records it contains, separated by a comma.
   Example:
   ```
   chunk_001.log,5
   chunk_002.log,4
   ```

Write, compile, and run the C++ program to perform this extraction and splitting. Make sure the output directory exists before writing to it.