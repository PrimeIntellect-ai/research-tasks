You are an engineer tasked with debugging and fixing a Go-based log processing service located in `/home/user/logprocessor`. 

The service is designed to parse a directory of CSV logs, extract the integer value from the second column of each line, and sum these values together. The final sum should be written to `/home/user/processed_output.txt`. Additionally, if any file contains corrupted lines that prevent parsing, the service is supposed to skip the file and append its absolute path to `/home/user/corrupted_files.txt`.

However, the service currently has three major issues that you need to investigate and fix:
1. **Compilation Error**: The codebase currently does not compile due to a function naming/linking mismatch between the main package and the `processor` package.
2. **Corrupted Input Panic**: The service reads data from `/home/user/data/`. At least one of the files in this dataset has a space in its filename and contains corrupted data. Processing it currently results in a runtime panic (index out of range) instead of gracefully returning an error. You must fix the code so it catches/prevents the panic, returns an error for the corrupted file, and allows the main loop to write the file's name to `/home/user/corrupted_files.txt`.
3. **Memory Leak**: The service is meant to be a long-running process but has a severe memory leak, causing its memory footprint to grow linearly with the number of files processed. Profile or analyze the code in `processor/process.go` and fix the leak so that the service's memory usage remains low and stable.

Your objectives:
1. Fix the compilation error.
2. Fix the runtime panic caused by corrupted data.
3. Fix the memory leak.
4. Run the program (`go run main.go`) successfully.

If you have completed the task correctly, the program will terminate cleanly, `/home/user/processed_output.txt` will contain the correct total sum, and `/home/user/corrupted_files.txt` will contain the absolute path(s) of the corrupted file(s).