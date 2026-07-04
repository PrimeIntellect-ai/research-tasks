You are an analyst tasked with processing monthly sales data that has been exported with problematic encoding.

You have a wide-format CSV file located at `/home/user/sales_wide.csv` containing monthly sales data for various stores. Unfortunately, the export tool encoded non-ASCII characters in the `store_name` column as Unicode escape sequences (e.g., `\u00e9` instead of `é`). 

You need to write a Go program `/home/user/process.go` that performs a multi-stage data processing pipeline:
1. **Normalization**: Read the CSV and decode the Unicode escape sequences in the `store_name` column back to standard UTF-8 characters.
2. **Reshaping**: Transform the data from wide format to long format. The output records should represent a single month's sales per store. The long format fields should be conceptually: `StoreID`, `StoreName`, `Month` (which is the exact column header, e.g., "jan_2023"), and `Sales`.
3. **Template Generation**: Apply the provided Go text template at `/home/user/report.tmpl` to each of the long-format records. Write the rendered output for all records sequentially to `/home/user/report.txt`, ensuring there is exactly one blank line between each rendered record block.
4. **Logging**: Write a log entry to `/home/user/process.log` containing exactly the string `Records processed: N` where `N` is the total number of long-format records successfully created and rendered.

Run your Go program to generate the required `report.txt` and `process.log` files.

Details:
- The CSV has headers. The first two columns are `store_id` and `store_name`. The remaining columns are monthly sales figures.
- Only process the sales columns that are present (do not hardcode the month names, as the script should work if new months are added).