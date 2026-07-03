I am a researcher organizing a massive dataset of sensor readings. I have a custom tool located at `/app/txt2csv-tools-1.2` that converts raw `.dat` files to `.csv`. However, the tool seems to be broken out of the box and throws an error when run.

Please help me accomplish the following data processing pipeline using Bash:

1. **Fix the Vendored Tool**: Identify and fix the bug in the package at `/app/txt2csv-tools-1.2/convert.sh` so it functions correctly. 
2. **Write the Pipeline**: Create a bash script at `/home/user/organize.sh`. This script must process all `.dat` files found in `/home/user/raw_data/`.
3. **Atomic Writes**: For each file, run the fixed `convert.sh <input_file>` and save the standard output as a `.csv` file in `/home/user/processed/` with the same base name (e.g., `sensor_1.dat` becomes `sensor_1.csv`). You **must** use atomic writes (e.g., redirect output to a temporary file or use memory-mapped/streamed pipes to a tmp file, then `mv` to the final destination) to ensure partial files are never visible in the `processed/` directory.
4. **Symbolic Linking**: The first line of each output `.csv` file will always contain a date header in the format `YYYY-MM-DD`. Your script must read this date and create a symbolic link in `/home/user/by_date/<YYYY-MM-DD>/<filename>.csv` pointing back to the corresponding file in `/home/user/processed/`. Ensure the date directories are created as needed.
5. **Performance Optimization**: There are thousands of files. Processing them sequentially with a standard `for` loop will take too long. You must optimize `/home/user/organize.sh` using parallel processing (e.g., `xargs -P` or GNU `parallel`) so that the entire dataset is processed rapidly.

Ensure `/home/user/organize.sh` is executable. The automated tests will measure the execution time of your script to ensure it meets our strict performance threshold.