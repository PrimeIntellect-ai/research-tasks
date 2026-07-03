I am a researcher dealing with a batch of poorly formatted sensor data files in `/home/user/dataset`. I need you to clean them up and organize them based on hidden metadata.

Here is what you need to do:

1. **Clean the headers**: Every `.dat` file in the `/home/user/dataset` directory has exactly 10 lines of useless text headers at the top. Use shell commands (like `sed` or `awk`) to permanently remove the first 10 lines from every `.dat` file in place.
2. **Extract Experiment IDs using Memory-Mapping**: Each file contains a hidden experiment ID embedded deep within the data lines. The ID is always exactly 8 alphanumeric characters and is immediately prefixed by the string `MAGIC_SIG:`. Because these files can theoretically be very large, you must write a Python script that uses the `mmap` module to efficiently search for the `MAGIC_SIG:` byte string and extract the 8-character ID that follows it.
3. **Rename the files**: Once you have the ID for a file, rename the cleaned file to `<EXPERIMENT_ID>.dat`. For example, if a file contains `MAGIC_SIG:X9Y8Z7W6`, it should be renamed to `X9Y8Z7W6.dat`. 
4. **Create a summary log**: After renaming all files, list the new file names (just the base names, e.g., `X9Y8Z7W6.dat`) in alphabetical order and save them to `/home/user/summary.log`, with one filename per line.

Requirements:
- All operations should happen in `/home/user/dataset`.
- You must use Python's `mmap` module for the extraction step to demonstrate memory-mapped I/O.
- The original filenames (e.g., `raw_data_*.dat`) should no longer exist at the end of the process.