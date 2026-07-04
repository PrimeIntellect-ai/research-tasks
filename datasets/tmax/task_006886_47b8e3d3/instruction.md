You are an artifact manager curating a binary repository. Compile systems frequently drop new ELF binaries into a staging directory, but sometimes these files are identical in execution behavior (represented by their entry point) or are still actively being written. 

Your task is to write a C program that reliably processes these files, performing deduplication via hard links and managing a rolling "latest" symlink, while avoiding race conditions with files currently being written.

Write a C program at `/home/user/curator.c` and compile it to `/home/user/curator`.

When run, the program must do the following:
1. Scan the input directory `/home/user/artifacts_in`. To ensure deterministic behavior, process the files in alphabetical order (e.g., using `scandir` with `alphasort`).
2. Ignore the `.` and `..` directories, and crucially, ignore any file whose name ends with the `.tmp` extension (these are actively being written and must not be touched).
3. For each valid file, read its header to determine if it is a valid 64-bit ELF binary. You must check that:
   - The first 4 bytes are the ELF magic number (`\x7fELF`).
   - The class is 64-bit (`ELFCLASS64`).
   If a file is not a valid 64-bit ELF, skip it.
4. If it is a valid 64-bit ELF, extract its entry point address (`e_entry` from `Elf64_Ehdr` in `<elf.h>`). We will use the entry point as our deduplication key.
5. Publish the artifact to `/home/user/artifacts_repo/` under the *exact same filename* it had in the input directory.
   - **Deduplication:** If this is the *first* time during this run you are seeing this specific `e_entry` address, perform a standard file copy from `artifacts_in` to `artifacts_repo`.
   - **Hard linking:** If you have already processed a file with this exact `e_entry` earlier in the current execution, do *not* copy the file. Instead, create a **hard link** in `artifacts_repo` with the new filename, pointing to the earlier file in `artifacts_repo` that shares this entry point.
6. **Symlinking:** After successfully copying or hard-linking an ELF binary, update the symbolic link at `/home/user/artifacts_repo/latest.elf` to point to this newly published file in the repository. The symlink should be updated for *every* valid processed ELF. If `latest.elf` already exists, overwrite it atomically or remove and recreate it.

**Constraints & Details:**
- You do not need to keep track of state between executions; the in-memory tracking of seen `e_entry` values only needs to last for the duration of a single run of your program.
- Use standard C libraries and `<elf.h>`.
- The input and repository directories will already exist. 
- You must compile your program with `gcc /home/user/curator.c -o /home/user/curator`. 
- Finally, execute your program `/home/user/curator` once to process the current state of `/home/user/artifacts_in`.