You are tasked with updating and extracting active configurations from a legacy configuration management archive. 

Your tasks are to:
1. Navigate to `/home/user/config_archive/`. You will find an archive named `legacy_configs.tar.gz`. Extract it.
2. Inside the archive is a single large configuration file named `system_master.ini`. This file is encoded in `ISO-8859-1`. Convert its character encoding to `UTF-8` and save the converted output to `/home/user/config_archive/system_master_utf8.ini`.
3. Write a C program named `/home/user/split_config.c` and compile it to `/home/user/split_config`. This program must read `/home/user/config_archive/system_master_utf8.ini` and split it into smaller files named `module_00.ini`, `module_01.ini`, `module_02.ini`, and so on. 
   - A new chunk file should be created every time a line starting exactly with `[MODULE_` is encountered.
   - The line starting with `[MODULE_` must be the first line of the new chunk.
   - The generated files should be saved in `/home/user/config_archive/`.
4. Create a directory at `/home/user/active_configs/`.
5. Check each of the generated `module_XX.ini` files. If a file contains a line with exactly `status=active`, create a symbolic link in `/home/user/active_configs/` pointing to the absolute path of that module file (the symlink should have the same name, e.g., `module_00.ini`).
6. Finally, concatenate all the files referenced by the symlinks in `/home/user/active_configs/` (in alphabetical order by filename) into a single merged file at `/home/user/active_master.ini`.

Ensure the final `active_master.ini` is in pure UTF-8 and contains only the modules that are explicitly marked as active.