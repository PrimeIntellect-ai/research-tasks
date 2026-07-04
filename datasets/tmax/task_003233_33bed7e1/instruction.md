You are acting as an artifact manager for a continuous integration system. You need to curate binary artifacts stored in a local repository while ignoring the "live" artifact that is currently being written by a simulated racing process.

You have a directory structure located at `/home/user/repo`. Inside this directory, there are multiple subdirectories containing binary artifact files, all ending with the `.dat` extension. One of these files is named `active.dat` (it could be anywhere in the repository structure). This file is currently "hot" and must be ignored.

Your task is to:
1. Write a C++ program (saved as `/home/user/archiver.cpp`) that recursively traverses `/home/user/repo`.
2. Find all `.dat` files, but strictly ignore any file named `active.dat`.
3. Sort the absolute paths of the discovered valid files in standard alphabetical order.
4. Read the contents of each valid file in that sorted order, and write their raw binary contents directly to `stdout`.
5. Compile the C++ program using C++17 or later (e.g., `g++ -std=c++17 /home/user/archiver.cpp -o /home/user/archiver`).
6. Run your compiled program and pipe its standard output through `gzip` to create a compressed archive at `/home/user/curated_archive.gz`.
7. Verify your archive by decompressing the stream and calculating its SHA-256 checksum. Write ONLY the 64-character SHA-256 hash to a file named `/home/user/checksum.txt`.

Ensure your C++ program does not print any extraneous text or debug information to `stdout`, as it will corrupt the binary stream being compressed.