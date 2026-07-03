I am a researcher trying to organize a massive archive of experimental data. My lab stores experimental metadata directly inside the compiled simulation binaries (ELF files) using a custom ELF section called `.exp_data`. Over time, these binaries have been dumped into a large, messy directory alongside logs, scripts, and other random files.

I need you to help me extract, clean, and archive this data.

Here is what you need to do:
1. **Write an ELF Parsing Tool:** Create a C program at `/home/user/extractor.c` that takes a file path as a command-line argument. It must parse the ELF file, locate the section named `.exp_data`, and print its exact raw string contents to `stdout`. (Assume all relevant binaries are 64-bit ELF executables for Linux, so you can use `<elf.h>`). Compile this tool to `/home/user/extractor`.
2. **Search and Extract:** The messy archive is located at `/home/user/dataset_archive`. Search through this directory (and its subdirectories) to find all ELF executable files. Use your `extractor` tool to read the `.exp_data` section from each ELF file that has one.
3. **Data Transformation:** The data inside the `.exp_data` sections is stored in a proprietary formatted string like this: `[TRIAL:001;OUTCOME:success;TIME:162341]`. 
   Using standard stream redirection, piping, and text-editing tools (like `sed`, `awk`, or `tr`), process the extracted raw data from all valid ELF files and compile it into a single, clean CSV file at `/home/user/summary.csv`.
   The CSV must have exactly this header: `trial,outcome,time` followed by the extracted values on separate lines. For example:
   ```csv
   trial,outcome,time
   001,success,162341
   ```
4. **Archive:** Finally, compress the `summary.csv` file into a gzip-compressed tarball located at `/home/user/final_archive.tar.gz`.

Requirements:
- Your C program must strictly use the ELF format specification to find the section (do not just `grep` the binary file, as the data might contain arbitrary bytes before the string).
- The final `summary.csv` should not contain duplicate lines and must be sorted alphabetically by the `trial` column.

Please complete all these steps. I will verify your work by checking the contents of `/home/user/final_archive.tar.gz` and the source code of your C parser.