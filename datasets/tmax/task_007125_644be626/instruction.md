As a data analyst, I frequently receive poorly formatted CSV files from an upstream data provider. Our downstream legacy system crashes if it encounters newline characters within data fields, and we also need to eliminate duplicate user entries before importing.

Please write a Go script at `/home/user/process.go` and run it to process my dataset. 

Here are the requirements:
1. **Input**: Read the CSV file located at `/home/user/input.csv`. The file has headers: `ID,Name,Email,Comments`.
2. **Filtering (No Newlines)**: Our legacy system cannot handle embedded newlines. If *any* parsed field in a row contains a newline character (`\n`) or a carriage return (`\r`), you must silently drop the entire row.
3. **Deduplication**: We only want unique users based on their email address. Compute the MD5 hash of the **lowercase** `Email` field for each row. If you see a hash that has already been encountered in the file, drop the row. (The first occurrence should be kept).
4. **Output**: Write the surviving records to `/home/user/output.json` as a JSON array of objects. The keys of the JSON objects must exactly match the CSV headers (`ID`, `Name`, `Email`, `Comments`). All values should be strings. 

Once your script is written, compile and run it so that `/home/user/output.json` is generated.