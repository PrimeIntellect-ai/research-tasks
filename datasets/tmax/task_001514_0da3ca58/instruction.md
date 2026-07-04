You are tasked with building a configuration tracking workflow using Bash. 

You have been provided with a proprietary, stripped binary located at `/app/config_compiler`. This binary acts as a configuration manager that compiles human-readable text configuration files into a custom binary format. 

Your objective is to write a bash script at `/home/user/process.sh` that processes a directory of raw text configurations, compiles them using the binary, extracts metadata from the resulting binary headers, and organizes them using symbolic links.

Here are the requirements for `/home/user/process.sh`:
1. The script should take no arguments. It should read raw config `.txt` files from `/home/user/raw_configs/`.
2. For each `.txt` file, use `/app/config_compiler <input_txt_path> <output_bin_path>` to compile it. Save the compiled binaries in `/home/user/compiled/`. If the compiler exits with a non-zero status (e.g., due to an invalid config), skip that file and continue.
3. The output binaries contain a 16-byte header. Through reverse-engineering or experimentation, determine how the Configuration ID (integer) and Unix Timestamp (integer) are encoded in this header.
4. For each successfully compiled binary, extract the Configuration ID and Timestamp.
5. Convert the Timestamp into a `YYYY-MM-DD` date string.
6. Create a symbolic link in `/home/user/tracked_configs/<YYYY-MM-DD>/config_<ID>.bin` that points to the corresponding compiled binary in `/home/user/compiled/`. Create the date directories as needed.

All paths in your script should be absolute. Use only bash built-ins, coreutils, and standard Linux CLI tools (like `hexdump`, `od`, `awk`, `date`, etc.). Do not use Python, Perl, or other scripting languages for the main processing logic.

Your solution will be evaluated by running `/home/user/process.sh` and then calculating the percentage of correctly generated and placed symbolic links in `/home/user/tracked_configs/`.