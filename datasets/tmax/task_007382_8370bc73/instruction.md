I am a researcher working with a large dataset of 3D printing GCode files. My files are scattered across many subdirectories, and I need to extract, custom-compress, and archive a specific subset of them based on their metadata.

Here is what I need you to do:

1. Search through the directory `/home/user/dataset/` (and all its subdirectories) for any `.gcode` files that contain the exact substring `; Material: PETG` anywhere in their text.

2. For every file that matches this criteria, read its contents and apply a custom text compression algorithm. The algorithm rule is:
   - Scan the file's text content.
   - Any time a character repeats consecutively 3 or more times, replace that entire sequence of identical characters with `<char>*<count>`.
   - For example, `G1 X100.000` becomes `G1 X100.0*3`.
   - The sequence `;;;; Custom` becomes `;*4 Custom`. 
   - A sequence of exactly 2 consecutive characters (like `oo`) remains unchanged.
   - The matching is case-sensitive and applies to all characters (including spaces, but you do not need to span compressions across newline characters, you can treat the whole file as a single string and compress any consecutive characters including newlines if they repeat 3+ times).

3. Save the compressed versions of these files into a new directory: `/home/user/processed_dataset/`.
   - Keep the original basename of the file, but append `.cz` to it. (e.g., `print_1.gcode` becomes `print_1.gcode.cz`).
   - Do not recreate the nested directory structure; place all `.cz` files flatly inside `/home/user/processed_dataset/`.

4. Create a JSON metadata file at `/home/user/processed_dataset/summary.json`. 
   - This file must contain a single JSON object (dictionary) mapping the *original filename* (basename only, e.g., `print_1.gcode`) to its *original, uncompressed file size in bytes* (integer).

5. Finally, create a compressed tarball archive of the processed directory at `/home/user/final_archive.tar.gz`. The archive should contain the `processed_dataset` folder and its contents.

Please write and run the necessary Python scripts and shell commands to accomplish this.