I have a messy directory of compiled project artifacts at `/home/user/messy_project/` that contains a mix of source files, text logs, and compiled ELF binaries scattered across deeply nested subdirectories.

I need you to write a multi-language solution (e.g., a Python or Ruby script paired with necessary shell setup) to automatically organize these binaries without wasting disk space, while maintaining a perfectly consistent log.

Here are your specific instructions:
1. **Dependency Management**: You may install any standard parsing libraries (like `pyelftools` for Python) if you prefer native parsing over shell command wrappers, but it must be done within user-space.
2. **Recursive Traversal & Parsing**: Recursively traverse `/home/user/messy_project/`. Identify all valid ELF files. Parse their ELF headers to extract two specific fields:
   - **Machine**: e.g., "Advanced Micro Devices X86-64", "Intel 80386", "ARM"
   - **Type**: e.g., "EXEC (Executable file)", "DYN (Shared object file)"
3. **Link Management**: For every ELF file found, create a hard link to it in a new organized directory structure located at `/home/user/organized_elfs/`. 
   - The structure must be: `/home/user/organized_elfs/<machine_name>/<type_name>/<original_filename>`
   - Clean the `<machine_name>` and `<type_name>` by replacing spaces with underscores and removing parentheses. For example, "EXEC (Executable file)" becomes "EXEC_Executable_file".
   - Only use hard links (not symbolic links or copies) so inodes match and disk space is conserved. Ignore non-ELF files.
4. **Atomic Writes**: As you process the files, you must build an inventory mapping. Once traversal and linking are complete, write this inventory to `/home/user/organized_elfs/inventory.json`. You *must* do this using an atomic write (write to a temporary file in the same directory first, then atomically rename/move it to `inventory.json` to prevent partial writes in case of crashes).
   - The JSON should be an array of objects, where each object has keys: `"original_path"`, `"linked_path"`, `"machine"`, and `"type"`.

Please write the code, install any dependencies, execute the script, and ensure `/home/user/organized_elfs/inventory.json` is successfully created with the correct atomic implementation.