You are an AI assistant helping a climate researcher organize their dataset.

You have been provided with an archive located at `/home/user/dataset_work/measurements.tar.gz`. 
Please perform the following operations:

1. Extract the contents of `/home/user/dataset_work/measurements.tar.gz` into the directory `/home/user/dataset_work/extracted/`. Before extracting, it is good practice to verify the archive's integrity (e.g., testing the gzip compression). 
2. The extracted archive contains a file named `metadata.txt` (a CSV file with a header: `ID,Status,Temperature,Path`).
3. Using shell tools like `awk` or `sed`, filter `metadata.txt` to keep only the lines where the `Status` column is exactly `VALID`. Save these filtered lines (without the header) to `/home/user/dataset_work/extracted/valid_metadata.txt`.
4. Write a Go program at `/home/user/dataset_work/parser.go` that reads `/home/user/dataset_work/extracted/valid_metadata.txt`. 
5. The Go program should parse the `Temperature` (the 3rd column) of all the valid rows, calculate the average temperature as a float64, and output the result as a JSON file to `/home/user/dataset_work/result.json`.
   The JSON file must have exactly this format:
   `{"average_temperature": 24.2}` 
   (Format the average to exactly 1 decimal place).
6. Compile and run your Go program to produce the final `result.json` file.