You are an AI assistant helping a technical writer organize documentation and assets for a 3D printing farm. 

The writer has dumped a set of GCode files into `/home/user/raw_gcode/`. These files contain metadata in their headers, but they are currently disorganized. 

Your task is to write a Python script at `/home/user/organizer.py` that processes these files and creates an organized documentation structure using symbolic and hard links. This allows the technical writer to navigate the files by different categorizations without duplicating the large file contents.

Requirements for `/home/user/organizer.py`:
1. It must scan all `.gcode` files in `/home/user/raw_gcode/`.
2. It must parse the GCode files to extract metadata. Look within the first 20 lines of each file for comments in this exact format:
   `; PRINTER: <PrinterName>`
   `; MATERIAL: <MaterialName>`
   If a file is missing the `PRINTER` or `MATERIAL` metadata, use `Unknown` for the missing value.
3. For each file, the script should create two organized views in `/home/user/docs/`:
   a) A **symbolic link** view located at `/home/user/docs/by_printer/<PrinterName>/<MaterialName>/<filename>.gcode`. These symbolic links must point back to the original files in `/home/user/raw_gcode/`.
   b) A **hard link** view located at `/home/user/docs/by_material/<MaterialName>/<PrinterName>/<filename>.gcode`. These must be hard links to the original files.
4. The script should automatically create any necessary directories.

After writing and running your script, execute the standard `tree` command on the `/home/user/docs/` directory and save its output to `/home/user/docs_tree.txt` so the technical writer can review the final structure.

Note: Run the Python script and generate the tree output yourself. Do not wait for the user to run it.