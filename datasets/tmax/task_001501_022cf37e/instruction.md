I am a researcher organizing a dataset of 3D printer trajectories. My equipment generates GCode files, compresses them individually with gzip, and batches them into a single tarball. Unfortunately, a recent power surge corrupted some of the compressed archives, and the files are poorly named. 

I need you to write a Go program that processes this incoming dataset.

The dataset is located at: `/home/user/dataset_incoming/robotics_data.tar.gz`
The target directory for processed files should be: `/home/user/dataset_processed/`

Your Go program must perform the following tasks:
1. Extract the tarball and verify the integrity of each inner `.gcode.gz` file. Ignore and skip any corrupted gzip files.
2. For the valid, uncorrupted `.gcode.gz` files, stream the decompressed contents.
3. Parse the GCode line-by-line to calculate the total material extrusion. In these files, extrusion uses absolute positioning. You need to find all `G1` commands that contain an `E` parameter (e.g., `G1 X12.5 Y14.0 E45.2`) and determine the maximum `E` value reached in the file.
4. Write the uncompressed, parsed GCode to the target directory.
5. You must bulk rename the output files based on the parsed extrusion data. The new filename should be `<original_basename>_E<max_E_integer>.gcode`. For example, if the inner file was `bracket.gcode.gz` and the maximum `E` value found was `45.8`, the output file should be named `/home/user/dataset_processed/bracket_E45.gcode`. (Truncate the max `E` value to an integer by dropping the decimal).

Requirements:
- Only output the valid files.
- Ensure `/home/user/dataset_processed/` is created if it doesn't exist.
- Run your Go program to complete the processing. 
- You can write your Go code to `/home/user/process_dataset.go` and run it. 

Please perform this transformation dataset processing.