You are a data analyst working with a dataset of quarterly sales metrics. The data is currently sitting in a local staging directory, and you need to process it using C.

Your objectives:
1. **Transfer the Data**: Copy the file `/home/user/staging/sales_wide.csv` to your working directory `/home/user/workspace/`.
2. **Process the Data in C**: Write and compile a C program (save the source as `/home/user/workspace/process.c` and compile it to `/home/user/workspace/process`) that performs the following:
   - Reads the `sales_wide.csv` file. The file has a header and follows the format: `ID,Region,Q1,Q2,Q3,Q4`
   - Reshapes the wide format into a long format conceptually (i.e., treating each quarter's value as an individual data point for that Region).
   - Extracts features by **ignoring any negative values** (treat them as errors or returns that shouldn't contribute to total gross sales).
   - Groups the data by `Region` and calculates the total sum of valid sales for each region.
   - Sorts the aggregated results by the total sum in **descending** order.
3. **Generate Output**: Your C program must write the results to a new file at `/home/user/workspace/summary.csv`.
   - The output file must include a header: `Region,TotalSum`
   - Each subsequent row should contain the region name and its corresponding total sum as an integer.

Ensure your code handles basic CSV parsing appropriately (you may assume standard ASCII comma-separated values without quoted commas) and is strictly written in C. Run your compiled program to generate the final `summary.csv`.