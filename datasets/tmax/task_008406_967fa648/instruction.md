I am a researcher trying to organize a messy dataset of experiment logs. The data was given to me as a multi-part split archive located in `/home/user/raw_data/`. 

To make matters worse, a previous automated backup script went haywire and created circular symlink loops inside the dataset directories. Standard tools like `grep -r` just hang indefinitely.

I need you to do the following:

1. Reassemble the split archive parts in `/home/user/raw_data/` and extract the contents to a new directory `/home/user/dataset/`.
2. Write a C program at `/home/user/parse_dataset.c` that safely traverses the `/home/user/dataset/` directory tree. It must handle or ignore symlinks to avoid falling into infinite directory loops.
3. The C program should search for all files ending in `.log`. 
4. Read these log files and parse the multi-line records within them. The records follow this exact format:
```
BEGIN RECORD
Experiment: <Experiment_ID>
Status: <SUCCESS|FAILED>
Result: <Float_Value>
END RECORD
```
(Note: There may be multiple records per file, and they are always separated by the BEGIN/END markers).
5. Extract the `Experiment_ID` and `Result` only for records where the `Status` is exactly `SUCCESS`.
6. Your C program should output the extracted data to a CSV file at `/home/user/results.csv`. The file must have the header `Experiment,Result` and the rows must be sorted alphabetically by the `Experiment_ID`.

Compile your program, run it, and ensure `/home/user/results.csv` is generated correctly.