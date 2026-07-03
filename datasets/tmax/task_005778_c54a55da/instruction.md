You are tasked with writing a C++ utility for a configuration manager that tracks changes to a binary configuration file and updates system state accordingly.

Write a C++ program at `/home/user/config_watcher.cpp` and compile it to an executable named `/home/user/watcher`. 

Your program must do the following:
1. Use `inotify` to continuously watch the file `/home/user/app_config.bin` for modification events (`IN_MODIFY`).
2. Whenever the file is modified, the program must open the file and map it into memory using `mmap` (read-only). The file will always be exactly 256 bytes in size.
3. The first 64 bytes of the mapped memory contain an absolute directory path as a null-terminated ASCII string. Extract this path.
4. Using path manipulation, create a symbolic link at `/home/user/active_env` that points to the extracted path. If the symlink already exists, you must safely overwrite/update it to point to the new path.
5. Append the extracted path followed by a newline character (`\n`) to a log file at `/home/user/watcher.log` using standard C++ streaming I/O (`std::ofstream`).
6. Unmap the memory and wait for the next modification event. The program should run indefinitely.

Ensure your code is compiled to `/home/user/watcher` (e.g., `g++ -std=c++17 /home/user/config_watcher.cpp -o /home/user/watcher`). Do not run the watcher daemon yourself; the automated verification system will start it in the background, trigger modifications to `/home/user/app_config.bin`, and verify the outputs.