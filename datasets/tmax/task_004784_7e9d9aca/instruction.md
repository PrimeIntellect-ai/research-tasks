I have a disorganized folder of old CNC machine files and firmware dumps located at `/home/user/project_files`. The folder contains a mix of GCode files (`*.gcode`) and ELF binaries (`*.elf`). 

I need you to write a Go program at `/home/user/organizer.go` and run it to organize and extract metadata from these files. Your Go program must perform the following steps:

1. **Directory Traversal**: Recursively walk through `/home/user/project_files`.
2. **GCode Parsing & Encoding Conversion**: 
   - All `.gcode` files in the directory are encoded in `ISO-8859-1`. Read them and convert the text to `UTF-8`.
   - Extract the first 3 movement commands (lines starting with `G0` or `G1`) from each file.
   - Write these extracted lines to `/home/user/gcode_summary.txt`. The format for each file should be:
     `[filename]`
     `line1`
     `line2`
     `line3`
     (where `[filename]` is just the base name of the file, e.g., `part1.gcode`). Sort the entries alphabetically by filename.
3. **ELF Parsing**:
   - For all `.elf` files, parse the ELF header (you can use Go's standard `debug/elf` package).
   - Extract the Entry Point address of the binary.
   - Write the results to `/home/user/elf_summary.txt`. The format should be: `[filename]: 0x[entry_point_in_lowercase_hex]`. Sort the entries alphabetically by filename.
4. **Merging and Custom Compression**:
   - Read the contents of `/home/user/gcode_summary.txt` and `/home/user/elf_summary.txt`.
   - Concatenate them: the full contents of `gcode_summary.txt`, followed by a single blank line, followed by the full contents of `elf_summary.txt`.
   - Compress the concatenated string using Go's `compress/zlib` package.
   - Save the compressed binary output to `/home/user/final_summary.zlib`.

Once your Go code is written, build and run it so that `/home/user/final_summary.zlib` is generated successfully.