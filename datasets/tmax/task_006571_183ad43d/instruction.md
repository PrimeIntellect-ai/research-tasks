I am a technical writer organizing documentation and firmware assets for our open-source 3D printer project. I need your help to extract data from our asset files, link them correctly, and update our documentation index. 

Here is what I need you to do:

1. **Parse GCode Metadata (C++)**: 
   Write a C++ program at `/home/user/parser.cpp` and compile it to `/home/user/parser`. The program must read a GCode file specified via a command-line argument. It should parse the file line-by-line, look for comments that exactly match the format `; TIME:<integer>` (e.g., `; TIME:1200`), sum all the integer values found in these lines, and print *only* the final total integer sum to standard output.
   Run your compiled program on `/home/user/docs_project/model_v2.gcode` to calculate the total print time.

2. **Manage Links**:
   Inside the `/home/user/docs_project/` directory, there are two firmware files: `fw_v1.elf` and `fw_v2.elf`.
   - Create a symbolic link named `/home/user/docs_project/latest.elf` that points to `fw_v2.elf`.
   - Create a hard link named `/home/user/docs_project/model_backup.gcode` that points to `model_v2.gcode`.

3. **Update Documentation (Text Transformation)**:
   In the `/home/user/docs_project/` directory, there is an `index.md` file. Use a tool like `sed` to perform in-place replacements in this file:
   - Replace the exact placeholder string `{{PRINT_TIME}}` with the total print time sum you calculated using your C++ program.
   - Replace the exact placeholder string `{{LATEST_FIRMWARE}}` with the string `latest.elf`.

Make sure all files are saved and updated in place exactly as specified.