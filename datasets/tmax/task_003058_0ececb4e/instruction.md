You are a developer tasked with organizing backup files for a C++ project. Due to a previous flawed log-rotation and backup script that suffered from race conditions, many of the project's source code archives were written incompletely. 

Your goal is to write a C++ program that recursively traverses a specific directory, checks the integrity of every `.zip` archive it finds, and performs bulk renaming based on the integrity status.

Requirements:
1. Write a C++ program and save it to `/home/user/organize_archives.cpp`.
2. Compile it to an executable named `/home/user/organize_archives`.
3. The program must recursively search through the directory `/home/user/project_backups/` and all its subdirectories.
4. For every `.zip` file found, verify its archive integrity. You may invoke standard CLI tools (like `unzip -t`) from within your C++ code to check the integrity.
5. If the archive is completely valid, rename the file by appending `_verified` before the `.zip` extension (e.g., `source_v1.zip` becomes `source_v1_verified.zip`).
6. If the archive is corrupted or fails the integrity check, rename the file by appending `_corrupt` before the `.zip` extension (e.g., `source_v2.zip` becomes `source_v2_corrupt.zip`).
7. Run your compiled program so that the files in `/home/user/project_backups/` are renamed accordingly.

Ensure your program handles paths correctly and only targets `.zip` files. Do not delete any files; only rename them in their original directories.