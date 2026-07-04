As a backup administrator, I am currently migrating our old Write-Ahead Log (WAL) archives. Our legacy system used a custom utility to compress these logs before archiving them. Unfortunately, the source code for this utility has been lost, and all we have left is a stripped Linux binary located at `/app/wal_archive_tool`. 

We cannot rely on a black-box undocumented binary for our critical backup infrastructure. Your task is to reverse-engineer the behavior of this legacy tool and write a bit-for-bit compatible C++ replacement. 

Requirements:
1. Analyze the `/app/wal_archive_tool` binary (you have tools like `objdump`, `strings`, `strace`, `gdb`, and `hexdump` available). 
2. Determine its custom compression algorithm, archive format structure (including any magic bytes or integrity footers).
3. Write a C++ program located at `/home/user/custom_archive_tool.cpp`.
4. Compile your program to `/home/user/custom_archive_tool` (e.g., using `g++ -O2 /home/user/custom_archive_tool.cpp -o /home/user/custom_archive_tool`).

The tool takes exactly two arguments: the input file path and the output file path.
Usage: `/home/user/custom_archive_tool <input_file> <output_file>`

Your C++ implementation must produce strictly identical output files to the original `/app/wal_archive_tool` for any given input data. We will automatically test your compiled binary against the original using a fuzzing verifier to ensure exact behavioral equivalence.