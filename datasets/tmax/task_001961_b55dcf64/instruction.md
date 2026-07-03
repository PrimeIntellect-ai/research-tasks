I need help organizing and analyzing some archived project files. 

I have a compressed backup archive located at `/home/user/artifacts.tar.gz`. Inside this archive, there are several directories representing different build environments (e.g., `build_alpha/`, `build_beta/`). Each build directory contains:
1. An ELF executable named `main.elf`
2. A log file named `trace.log`

Please perform the following operations:
1. Write a Python script (or use bash commands) to process this archive without permanently extracting its entire contents to disk (you can extract files temporarily or process them as a stream).
2. For each `main.elf`, determine its entry point address (in hex format, e.g., `0x401000`). You can use `readelf` for this.
3. For each `trace.log`, count the number of multi-line critical error blocks. A critical error block starts exactly with the line `--- BEGIN CRITICAL ---` and ends exactly with `--- END CRITICAL ---`.
4. Generate a CSV report at `/home/user/report.csv` with the following header:
   `build_id,entry_point,error_count`
   Where `build_id` is the name of the directory (e.g., `build_alpha`). Sort the CSV rows alphabetically by `build_id`.
5. Finally, split the generated `/home/user/report.csv` into smaller chunks of exactly 40 bytes each using the `split` command. Place the output chunks in the directory `/home/user/chunks/` with the prefix `part_`.

Ensure all directory paths and file names match exactly as requested.