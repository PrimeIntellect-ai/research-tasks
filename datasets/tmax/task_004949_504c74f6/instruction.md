I'm organizing some project files and need your help dealing with nested archives and identifying binary files. 

I have an archive located at `/home/user/project_files.tar.gz`. This archive contains nested archives (specifically, a zip file inside the tar.gz). 

Please perform the following steps:
1. Extract the contents of `/home/user/project_files.tar.gz` into the directory `/home/user/extracted/`. If there are any nested archives (like `.zip` files) inside, extract their contents as well into the same `/home/user/extracted/` directory.
2. Remove the intermediate nested archives (e.g., `.zip` files) from `/home/user/extracted/` after extraction so only the final files remain.
3. Write a Go program at `/home/user/rename_elfs.go` that iterates through all files in `/home/user/extracted/`.
4. Your Go program must use the standard `debug/elf` package to parse each file. If a file is a valid ELF binary, the program should bulk rename it by appending its architecture (Machine type) to the filename, followed by the `.elf` extension. The architecture string must be exactly the default string representation of the `elf.Machine` constant (for example, `EM_X86_64` or `EM_AARCH64`). 
   - For example, an ELF file named `mybin` that targets x86_64 should be renamed to `mybin_EM_X86_64.elf`.
   - Files that are not valid ELF binaries (like text files) should be ignored and left with their original names.
5. Run your Go program to perform the renaming.

Ensure the final extracted directory only contains the properly renamed ELF files and the un-renamed non-ELF files.