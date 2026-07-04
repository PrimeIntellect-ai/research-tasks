You are assisting a scientific researcher in organizing real-time dataset ingestion. The researcher has a data-generating simulator that continuously writes fragments of sensor data to a directory. However, the simulator writes in chunks, which occasionally causes race conditions if a script tries to read the file before it's completely written. 

Your task is to write a Go program that safely watches for, processes, and cleans up these dataset files.

Create a Go program at `/home/user/aggregator.go` with the following requirements:
1. **File Watching**: It must continuously watch the directory `/home/user/incoming_data/` for new or modified `.csv` files.
2. **Metadata Search**: The simulator sets the executable bit (`+x`) on files while it is actively writing them, and removes the executable bit (`-x`) when the file is finalized. Your program must ONLY attempt to process `.csv` files that do NOT have the executable permission set for the owner.
3. **File Locking**: To absolutely guarantee no race conditions with the simulator's log rotation and cleanup functions, your program must attempt to acquire an exclusive, non-blocking file lock (using `syscall.Flock` with `LOCK_EX|LOCK_NB`) on the file. If it cannot acquire the lock, it should ignore the file and try again later.
4. **Data Processing**: Once safely locked and verified, read the file. Each line contains a single integer. Calculate the sum of all integers in the file.
5. **Output**: Append the calculated sum to a log file at `/home/user/processed_sums.log` exactly in this format: `<filename>:<sum>` (e.g., `data_01.csv:452`). `<filename>` should be the base name of the file, not the full path.
6. **Cleanup**: After successfully processing and logging the sum, delete the `.csv` file from the `incoming_data` directory.

You will need to initialize a Go module in `/home/user/` and install any necessary dependencies (like `github.com/fsnotify/fsnotify`). 

To test your code, we have provided a simulator script at `/home/user/simulator.sh`. 
Compile your Go program to `/home/user/aggregator`. 
Ensure your Go program is running in the background, then execute `/home/user/simulator.sh`. The simulator will run for approximately 10 seconds. After the simulator finishes, your Go program should have processed all the files, and `/home/user/processed_sums.log` should contain the correct totals.