You are tasked with migrating a legacy configuration management system to a new standardized format. This requires data transformation, encoding normalization, and reverse-engineering an old proprietary encoding tool.

Perform the following steps:

1. **Normalize Legacy Configurations**:
   There is a directory at `/home/user/legacy_configs` containing various legacy configuration files ending in `.conf`. These files were created on different systems and are in a mix of `ISO-8859-1` and `UTF-16LE` encodings.
   - Traverse the directory recursively.
   - Detect or safely convert the encoding of all `.conf` files to `UTF-8`.
   - Concatenate the contents of all `.conf` files (in alphabetical order of their absolute file paths) into a single file at `/home/user/all_configs.utf8`.

2. **Reverse Engineer the Encoder**:
   The system uses a proprietary encoding utility located at `/app/diff_encoder`. This is a stripped binary that reads from standard input and writes encoded data to standard output.
   - Analyze `/app/diff_encoder` to understand its encoding algorithm (it processes data in fixed-size chunks, performs specific bitwise and ordering transformations, and pads data when necessary).
   - Write a C program at `/home/user/solution.c` that exactly replicates the behavior of `/app/diff_encoder`.
   - Compile your program to `/home/user/encoder` (e.g., `gcc -O2 /home/user/solution.c -o /home/user/encoder`).

3. **Encode the Data**:
   - Pipe the contents of `/home/user/all_configs.utf8` through your `/home/user/encoder` program.
   - Save the final encoded output to `/home/user/encoded_configs.dat`.

An automated test suite will verify your work by checking the final output file and by fuzzing your `/home/user/encoder` binary against the original `/app/diff_encoder` with thousands of random inputs to ensure bit-exact equivalence.