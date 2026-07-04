You are assisting a data analyst who has been struggling with a Bash script. 

The analyst wrote a script located at `/home/user/analyze.sh` to process two CSV files: `/home/user/customers.csv` and `/home/user/purchases.csv`. Their goal was to calculate the total purchase amount for each region. However, their script uses a nested `while` loop that creates an implicit cross join, causing it to run extremely slowly and produce entirely incorrect, inflated numbers.

Your task is to rewrite `/home/user/analyze.sh` to efficiently join these files and aggregate the data. 

Requirements:
1. You must use standard Linux command-line tools (like `awk`, `join`, `sort`, `jq`, etc.) within the Bash script. Do not use Python, Perl, or other scripting languages.
2. `customers.csv` has the header: `customer_id,name,region`
3. `purchases.csv` has the header: `purchase_id,customer_id,amount`
4. Join the files on `customer_id`.
5. Calculate the total sum of `amount` for each `region`.
6. Output the final aggregated data as a single JSON object to the file `/home/user/region_summary.json`.
7. The JSON keys must be the region names, and the values must be the total purchase amounts (as numbers, not strings). 
   Example format:
   ```json
   {
     "North": 170.5,
     "South": 100
   }
   ```
8. Ensure your script properly skips the CSV headers.

Run your script to generate the `/home/user/region_summary.json` file once you are done.