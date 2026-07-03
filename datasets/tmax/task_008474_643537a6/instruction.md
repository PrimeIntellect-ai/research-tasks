I need help reorganizing and updating a legacy C++ project archive. The project files are currently stored in a tarball at `/home/user/legacy_project.tar`. 

Here is what you need to do:
1. Extract the contents of `/home/user/legacy_project.tar` into a new directory: `/home/user/workspace`.
2. The source files inside were written using the `ISO-8859-1` character encoding. Convert all `.cpp` and `.h` files in `/home/user/workspace` to `UTF-8` in-place.
3. The codebase contains an outdated macro. Use `sed` (or a similar text manipulation tool) to replace all occurrences of `OLD_MACRO_XYZ` with `NEW_MACRO_ABC` across all the `.cpp` and `.h` files.
4. Create a directory `/home/user/workspace/include`. Inside this directory, create symbolic links to every `.h` file present in the root of `/home/user/workspace`. The symlink names must match the original header file names.
5. Write a C++ program at `/home/user/pack.cpp` and compile it to `/home/user/pack`. This program should pack the updated `.cpp` and `.h` files (ignore directories and symlinks) into a single custom binary archive located at `/home/user/final.bin`. 
   For each file, the binary format must be:
   - 1 byte: The length of the filename (e.g., `8` for `main.cpp`).
   - N bytes: The filename itself (e.g., `main.cpp`).
   - 4 bytes: The size of the file contents in little-endian format (uint32_t).
   - M bytes: The raw file contents.
   The files should be written into the binary archive in alphabetical order of their filenames.

Once you have generated `/home/user/final.bin` and set up the symlinks, the task is complete.