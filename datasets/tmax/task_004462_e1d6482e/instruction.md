You are assisting a materials researcher in organizing a messy dataset of 3D printing experiment logs. 

The dataset is located at `/home/user/printing_dataset/`. Due to a previous script error, the directory structure contains several symlink loops (e.g., directories linking back to their parents) which can cause infinite recursion if not handled properly. The dataset contains `.gcode` files (text-based 3D printing instructions), `.elf` compiled binaries (which you should ignore), and other miscellaneous files.

Your task is to write and execute a Python script that accomplishes the following:

1. **Safe Traversal:** Recursively traverse `/home/user/printing_dataset/` to find all files ending with `.gcode`, while safely ignoring or avoiding symlink loops.
2. **Format Parsing:** Parse each found `.gcode` file to extract the total filament used. In these files, the filament usage is recorded exactly in a comment line formatted as: `; filament_used_mm: <value>` (e.g., `; filament_used_mm: 142.5`). If a `.gcode` file does not contain this exact metadata line, skip it.
3. **Bulk Renaming:** Rename each valid `.gcode` file to include the filament usage. The new filename should be `<original_basename>_<value>mm.gcode`. For example, `experiment1.gcode` becomes `experiment1_142.5mm.gcode`. The file must remain in its original directory.
4. **Atomic Summary:** Create a consolidated JSON report mapping the **new absolute file paths** to their corresponding float values of filament used. 
   - The JSON should be a flat dictionary: `{"/home/user/printing_dataset/nested/experiment1_142.5mm.gcode": 142.5, ...}`
   - To prevent data corruption during the researcher's automated backups, you **must** write this JSON file atomically. Write the data to `/home/user/printing_summary.json.tmp` first, and then rename it to `/home/user/printing_summary.json`.

Ensure your script runs successfully and leaves the system in the requested state.