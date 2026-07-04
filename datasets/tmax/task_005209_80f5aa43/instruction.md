I am a storage administrator for a large 3D printing farm. We are running out of disk space on our primary storage array. I've isolated the issue to a directory of bloated, gzip-compressed GCode files at `/home/user/bloated_gcode/`. Due to a misconfiguration in an older slicer, these files were saved in UTF-16LE encoding and contain massive, unnecessary comment blocks before being compressed.

I need you to write a Rust utility to stream-process these files, minimize them, and recompress them to save space. 

Please follow these steps:
1. Create a new Rust project in `/home/user/minimizer/`.
2. Write a Rust program that reads all `.gcode.gz` files in `/home/user/bloated_gcode/`.
3. For each file, the program must:
   - Decompress the gzip stream.
   - Decode the text from UTF-16LE to UTF-8.
   - Strip all comments. A comment begins with a `;` character and continues to the end of the line. Remove the `;` and all subsequent characters.
   - Trim any trailing spaces or tabs from the remaining line.
   - If a line becomes completely empty after comment removal and trimming, discard the line entirely.
   - Re-compress the minimized UTF-8 text using gzip.
   - Save the newly compressed file to `/home/user/minimized_gcode/` using the exact same filename.
4. Run your Rust program to process the files.
5. Finally, generate a SHA256 manifest of the newly created compressed files in `/home/user/minimized_gcode/` and save it to `/home/user/manifest.txt`. The manifest should be generated using standard Linux tools (e.g., `sha256sum`) and contain lines formatted exactly as: `<hash>  <filename>`. Run this command from within the `/home/user/minimized_gcode/` directory so the filenames in the manifest do not contain full paths.

Constraints:
- You must use Rust as the primary language to process the files. You may use external crates (like `flate2`, `encoding_rs`, etc.) by adding them to your `Cargo.toml`.
- Ensure `/home/user/minimized_gcode/` is created before saving files.