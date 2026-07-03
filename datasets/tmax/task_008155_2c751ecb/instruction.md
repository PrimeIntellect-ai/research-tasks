I have a project directory at `/home/user/gcode_files` containing several 3D printing `.gcode` files. I need to quickly find the prints that will finish fast and package them up for my print server.

Please do the following:
1. Write a C++17 program at `/home/user/organize.cpp` that iterates through all files in `/home/user/gcode_files`.
2. For every file, parse its contents to find a line starting exactly with `; LAYER_COUNT:` followed by an integer (e.g., `; LAYER_COUNT: 45`). 
3. If the layer count is strictly less than 50, create a **hard link** to this file inside `/home/user/quick_prints/` using the exact same filename.
4. Compile your program (e.g., to `/home/user/organize`) and run it.
5. After the program finishes, use standard shell commands to archive the `quick_prints` directory into a gzip-compressed tarball located at `/home/user/quick_prints.tar.gz`. When extracted, the tarball should output the `quick_prints` directory and its contents (e.g. `quick_prints/file.gcode`).

Ensure your C++ program gracefully ignores files that don't have the layer count metadata or are not standard files. You can assume all layer count lines follow the exact format `; LAYER_COUNT: <number>`.