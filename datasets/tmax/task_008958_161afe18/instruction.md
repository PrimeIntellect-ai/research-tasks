I have a messy project archive that needs to be organized, updated, and repackaged. The archive is located at `/home/user/messy_project.tar.gz`.

Please perform the following operations using standard Linux terminal tools:

1. Create a directory called `/home/user/workspace` and extract the contents of `/home/user/messy_project.tar.gz` into it.
2. Recursively find and decompress any `.gz` files (that are not tarballs) located inside `/home/user/workspace` so they become plain files.
3. Identify all ELF executables/binaries inside `/home/user/workspace` (note: they might not have a typical file extension, or they might have misleading extensions). 
4. Create a directory at `/home/user/binaries`. Move all the identified ELF binaries from `/home/user/workspace` into `/home/user/binaries`.
5. After moving the binaries, search through all remaining files in `/home/user/workspace`. You will find a deprecated macro `OLD_MACRO_XYZ()`. Replace every occurrence of this exact string with `NEW_MACRO_ABC()` across all files in the workspace. Modify the files in-place.
6. Create a zip archive of the `/home/user/binaries` directory, saving it to `/home/user/binaries_archive.zip`. The zip should contain the files at its root (do not include the full absolute path inside the zip).
7. Create a bzip2-compressed tarball of the cleaned `/home/user/workspace` directory, saving it to `/home/user/workspace_clean.tar.bz2`.
8. Create a log file at `/home/user/elf_list.txt` containing only the base filenames of all the ELF binaries you moved, with one filename per line, sorted alphabetically.

Ensure all file replacements are saved correctly and the archives are properly constructed.