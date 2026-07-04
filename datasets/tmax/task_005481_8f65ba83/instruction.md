You are a data engineer building a local ETL pipeline to process export files from a legacy system. 

A legacy application is currently serving a daily transaction log over HTTP. The file is located at `http://localhost:8080/transactions.csv`. 

Because it's a legacy system, the CSV file is encoded in UTF-16LE. 

Your task is to write and execute a series of Bash commands to accomplish the following:
1. Download the file from `http://localhost:8080/transactions.csv`.
2. Convert the file's encoding from UTF-16LE to standard UTF-8.
3. The CSV has a header row: `tx_id,category,amount`. Ignore the header row for calculations.
4. Calculate the total `amount` for each `category`.
5. Sort the resulting summary alphabetically by category name.
6. Save the final aggregated data to exactly this file path: `/home/user/category_totals.txt`.

The output file `/home/user/category_totals.txt` must have exactly the following format for each line:
`<Category>: <TotalAmount>`
(Example line: `Electronics: 400.50`)

Ensure the totals are formatted to exactly two decimal places. Use standard Bash tools (like `curl`, `wget`, `iconv`, `awk`, `sort`, etc.) to complete this task.