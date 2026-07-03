You are an AI assistant acting as a configuration manager for a manufacturing facility. We track changes to our `.gcode` manufacturing files using a custom incremental backup system.

Your task is to write and execute a C++ program that generates a new manifest of our GCode files, identifies which files have changed since the last manifest, and creates an incremental backup archive.

Here are the specific requirements:

1. **Workspace setup:** 
   The current GCode files are located in `/home/user/gcode_current/`.
   The previous manifest is located at `/home/user/manifest_v1.txt`.

2. **C++ Program Requirements:**
   Create a C++ program at `/home/user/tracker.cpp` and compile it to `/home/user/tracker`. 
   The program must accept four command-line arguments:
   `./tracker <old_manifest_path> <current_gcode_dir> <new_manifest_out_path> <archive_out_path>`

3. **Parsing and Manifest Generation:**
   The program must scan `<current_gcode_dir>` for all `.gcode` files.
   For each file, it must:
   - Parse the file to extract the version. The version is always on the first line of the file in the exact format: `;; VERSION: <version_string>`. If this header is missing or malformed, default the version to `UNKNOWN`.
   - Calculate the SHA-256 checksum of the file's entire contents. You may invoke external shell commands like `sha256sum` from within your C++ program or use a library.
   
4. **Incremental Logic:**
   The program must read `<old_manifest_path>`. The manifest format is a CSV-like text file where each line is:
   `filename,version,sha256`
   (Note: `filename` is just the base name of the file, e.g., `partA.gcode`).
   
   Compare the current files against the old manifest. A file is considered "NEW_OR_CHANGED" if:
   - It is not present in the old manifest.
   - OR its SHA-256 checksum differs from the checksum in the old manifest.

5. **Outputs:**
   - **New Manifest:** Write the new state to `<new_manifest_out_path>` using the exact same format (`filename,version,sha256`). The lines must be sorted alphabetically by `filename`.
   - **Incremental Archive:** The program must package all "NEW_OR_CHANGED" files into a compressed tarball (`.tar.gz`) at `<archive_out_path>`. The archive should store the files at its root (no leading directory paths, e.g., `tar -tzf archive.tar.gz` should output just the filenames like `partB.gcode`).

Execute your compiled C++ program as follows:
`./tracker /home/user/manifest_v1.txt /home/user/gcode_current /home/user/manifest_v2.txt /home/user/incremental.tar.gz`

Ensure all output files are created successfully and have the correct permissions.