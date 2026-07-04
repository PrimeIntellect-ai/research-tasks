I have a directory of old CNC project files that I need to organize and analyze. The files are located in `/home/user/projects/cnc_data/` and have a `.rle` extension.

These files were compressed using a custom, primitive Run-Length Encoding (RLE) tool, and the original text inside was encoded in UTF-16LE. 

I need you to write a Go program (save it as `/home/user/process_gcode.go`) that does the following:
1. Iterates through all `.rle` files in `/home/user/projects/cnc_data/`.
2. Decompresses the custom RLE format. The format consists of 2-byte pairs: `[Count][Byte]`. The `Count` is an unsigned 8-bit integer representing how many times the `Byte` should be repeated. (e.g., `0x03 0x41` means "AAA").
3. Decodes the resulting decompressed byte stream from UTF-16LE into UTF-8.
4. Parses the resulting UTF-8 text as GCode. 
5. Counts the number of `G1` movement commands in each file. A `G1` command is defined as any line where the first non-whitespace sequence of characters is exactly `G1` (case-sensitive).
6. Writes the results to a log file at `/home/user/gcode_summary.txt`.

The output file `/home/user/gcode_summary.txt` must contain one line per file, formatted exactly as `[original_filename].gcode: [count]`, sorted alphabetically by the filename. For example, if `part1.rle` had 15 `G1` commands, its line would be `part1.gcode: 15`.

Please compile and run your Go program to generate the required `/home/user/gcode_summary.txt` file.