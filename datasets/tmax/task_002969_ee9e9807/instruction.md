You are a backup administrator recovering executable files from a partially corrupted disk dump. Your task is to extract valid ELF binaries from a recovery directory, rename them systematically based on their internal metadata, and create a verified backup archive.

The recovered data is located at `/home/user/recovered_data`. It contains a mix of nested directories, regular text files, corrupted files, and valid ELF executables.

Perform the following steps using Bash and standard Linux utilities:

1. **Recursive Traversal & Parsing**: Search through `/home/user/recovered_data` and all its subdirectories to find valid ELF files. For each valid ELF file, extract its "Build ID" (a hexadecimal string) using the `readelf` utility. If a file is not an ELF file, is corrupted, or does not have a Build ID, ignore it.
2. **Bulk Renaming & Organization**: Create a new directory `/home/user/clean_backup`. Copy every valid ELF file you found into this directory. When copying, rename the file to follow this exact format: `<original_filename>_<build_id>.elf` (for example, if the original file is `app_bin` and its Build ID is `abcdef123`, the new name should be `app_bin_abcdef123.elf`).
3. **Archive Creation**: Create a gzip-compressed tar archive named `/home/user/elf_backup.tar.gz` containing all the files inside `/home/user/clean_backup` (do not include the `clean_backup` directory itself in the archive paths, only the files).
4. **Archive Integrity Verification**: Verify the integrity of the tarball. Write the names of the files successfully stored in the archive (one per line, just the filenames without paths) to a log file at `/home/user/archive_contents.txt` sorted alphabetically.

Ensure your script is robust against files with spaces in their names (though the setup may or may not have them, standard bash best practices apply).