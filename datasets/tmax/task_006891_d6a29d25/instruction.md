You are helping organize a monolithic binary asset file for a game project by splitting it into smaller, manageable files based on a configuration file. 

Your task is to write a C++ program to parse the configuration and split the binary file, and then generate a checksum manifest.

1. Write a C++ program at `/home/user/split_assets.cpp`.
2. The program must read an existing configuration file located at `/home/user/split_config.txt`. The config file contains lines formatted as:
   `<filename> <size_in_bytes>`
3. The program must open the existing binary data file at `/home/user/project_data.bin`.
4. Reading `project_data.bin` sequentially from the beginning, the program must extract the exact number of bytes specified for each file in the config, and write them into the `/home/user/output/` directory using the specified `<filename>`.
5. Any remaining, unread bytes at the end of `project_data.bin` (after processing all entries in the config file) must be written to a file named `/home/user/output/remainder.bin`.
6. Compile and run your C++ program to perform the splitting.
7. After the files are split, generate a standard SHA256 manifest file at `/home/user/output/manifest.sha256` that contains the checksums for all `.bin` files located in the `/home/user/output/` directory. Use standard tools to create this manifest.

Make sure your C++ code handles file parsing and binary file I/O correctly.