You are tasked with organizing and transforming a set of 3D printing project files for a prototype. The workflow requires extracting data, parsing metadata from a blueprint, transforming GCode files concurrently, and packaging the results.

Follow these steps exactly:
1. **Extract Metadata**: Analyze the blueprint image located at `/app/blueprint.png`. Use OCR (e.g., `tesseract`) to extract the numeric scale factor written on it. Look for the text "SCALE: ".
2. **Unpack Data**: Extract the archive `/app/data.tar.gz` into `/home/user/raw_data`. It contains a messy hierarchy of files.
3. **Filter Project Files**: You only need to process valid GCode files. A valid project file is any file in `/home/user/raw_data` (and its subdirectories) that has the `.gcode` extension AND contains the exact string `; TYPE: PART` within its first 5 lines.
4. **Transform via C Program**: Write a C program `scaler.c` and compile it to `/home/user/scaler`. 
   - The program should accept 3 arguments: `input_file`, `output_file`, and `scale_factor`.
   - It must parse the input GCode file line by line.
   - For every line, if it contains `X`, `Y`, or `Z` coordinates (e.g., `G1 X10.5 Y20.0 Z1.0 E0.5`), multiply the numeric value of the X, Y, and Z coordinates by the `scale_factor`. Other commands and parameters (like `E`, `F`, `G`) should remain unchanged.
   - Output the modified lines to the `output_file`. Format the scaled coordinates to exactly 3 decimal places (e.g., `X18.375`).
   - Concurrency requirement: After successfully writing the output file, the C program must append a log entry `PROCESSED: <input_filename>` (just the basename of the file) to a shared log file at `/home/user/process_wal.log`. Because this program will be run concurrently, you MUST implement POSIX file locking (using `fcntl` or `flock` in C) to acquire an exclusive lock on `/home/user/process_wal.log` before appending, and release it after, to prevent data corruption.
5. **Concurrent Execution**: Write a shell script `/home/user/run.sh` that finds all the valid GCode files, creates a directory `/home/user/scaled_data/`, and executes your `scaler` C program on all valid files concurrently (e.g., using `xargs -P 4` or bash background jobs). The output files should be saved in `/home/user/scaled_data/` with the same basenames.
6. **Package Results**: Create a ZIP archive of the transformed files at `/home/user/final_project.zip` containing the contents of `/home/user/scaled_data/` (just the files, no nested directories).

Ensure all scripts are executable and run them to produce the final `.zip` archive.