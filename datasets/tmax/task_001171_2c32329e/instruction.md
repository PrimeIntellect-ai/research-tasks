You are an artifact manager tasked with curating a messy binary repository. You have been provided with an archive of raw artifacts located at `/home/user/raw_artifacts.tar.gz`. 

Your goal is to extract this archive, analyze the files within it by parsing their formats and metadata, and organize the relevant artifacts into a new curated archive.

Here are your instructions:

1. Extract `/home/user/raw_artifacts.tar.gz` into the directory `/home/user/artifacts`.
2. Write a bash script at `/home/user/curate.sh` that recursively traverses the `/home/user/artifacts` directory.
3. Your script must create a directory structure at `/home/user/curated/` with three subdirectories: `elf`, `gcode`, and `wal`.
4. As your script traverses the artifacts, it should classify and copy files into the appropriate curated subdirectories based on the following rules:
   - **ELF Files**: Identify ELF binaries. If the ELF file is compiled for the "ARM" machine architecture (you can check this using tools like `readelf` or `file`), copy it to `/home/user/curated/elf/`.
   - **GCode Files**: Identify files with a `.gcode` extension. If the file contains the homing command `G28` (as a distinct word, e.g., `G28` or `G28 X Y`), copy it to `/home/user/curated/gcode/`.
   - **WAL Files**: Identify SQLite Write-Ahead Log (WAL) files. A valid SQLite WAL file always starts with the 4-byte magic number `0x377f0682` or `0x377f0683` (represented as bytes `37 7f 06 82` or `37 7f 06 83` in hex). Read the file header to verify this magic number. If it matches, copy the file to `/home/user/curated/wal/`.
5. Run your script to populate the `/home/user/curated` directory.
6. Once the directory is populated, compress the entire `/home/user/curated` directory into a zip archive located at `/home/user/curated_artifacts.zip`. Ensure the paths inside the zip archive are relative to `/home/user/curated` (i.e., the zip should contain the `elf`, `gcode`, and `wal` directories at its root).

Ensure your script is executable and runs successfully. Use standard Linux utilities available in the terminal.