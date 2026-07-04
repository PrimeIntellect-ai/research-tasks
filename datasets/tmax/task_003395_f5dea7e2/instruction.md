I am a researcher organizing a massive dataset of 3D printer logs. My dataset contains hundreds of GCode files, and I need to extract the spatial coordinates of all linear extrusion moves to analyze spatial distribution. Because the dataset is so large, I plan to process these files concurrently, but for now, I just have a small test dataset.

Please write a C program that meets these exact requirements:
1. The source code must be saved at `/home/user/extract_moves.c`.
2. The compiled executable should be at `/home/user/extract_moves`.
3. The program should accept exactly two command-line arguments: `<input_gcode_file>` and `<output_binary_file>`.
4. It should read the input GCode text file line by line.
5. It should parse lines that start exactly with `G1 ` (G1 followed by a space).
6. On those lines, it must look for `X` and `Y` coordinate values (e.g., `G1 X10.5 Y20.0 E1.5`). If a `G1` line contains both an `X` value and a `Y` value, it should extract them as single-precision floating-point numbers (`float`). If either X or Y is missing, ignore the line.
7. The program must open `<output_binary_file>` in append mode, apply an exclusive file lock using `flock()` or `fcntl()` to prevent race conditions during concurrent execution, and write the extracted X and Y values as a binary sequence of two `float`s (8 bytes total per matched line). Finally, it must release the lock and close the file.

Once you have written and compiled the program, I want you to run it concurrently on all `.gcode` files located in `/home/user/datasets/gcode_logs/` using the following exact command:
`find /home/user/datasets/gcode_logs/ -name "*.gcode" | xargs -n 1 -P 4 -I {} /home/user/extract_moves {} /home/user/datasets/combined_moves.bin`

Ensure that the final output file `/home/user/datasets/combined_moves.bin` contains the binary floats of all valid X and Y coordinates extracted from the logs.