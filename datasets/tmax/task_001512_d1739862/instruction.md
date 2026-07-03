You are a data analyst at a global retail company. We receive weekly sales data compiled from North America (NA), Europe (EU), and Asia (AS), but the data is messy, wide-formatted, and contains inconsistencies in how local product names are encoded. 

Your task is to process the raw data file located at `/home/user/raw_sales.csv` and generate a clean, aggregated summary file at `/home/user/summary.csv`.

Here are the details of what you need to do:

1. **Unicode Normalization:** The column `Product_Name_Local` contains text in various languages (including Latin, Cyrillic, and CJK characters). Due to encoding issues, some characters are decomposed or use full-width variants. Normalize all strings in this column using the NFKC (Normalization Form Compatibility Composition) standard. Name this new column `Normalized_Name`.

2. **Wide-to-Long Reshaping:** The raw CSV has sales and temperature data in a wide format: 
   Columns: `Date`, `Product_ID`, `Product_Name_Local`, `Sales_NA`, `Temp_NA`, `Sales_EU`, `Temp_EU`, `Sales_AS`, `Temp_AS`.
   Reshape this into a long format so that each row represents a single region's observation on a given date. The resulting columns should include `Date`, `Product_ID`, `Normalized_Name`, `Region`, `Sales`, and `Temp`. (`Region` should be one of "NA", "EU", or "AS").

3. **Interpolation & Imputation:** There are missing temperature (`Temp`) values (represented as empty strings). You must interpolate these missing values. Sort the long-format data by `Region` and then chronologically by `Date`. Then, apply linear interpolation to the `Temp` column *within each Region*. After interpolation, round all `Temp` values to 2 decimal places. 

4. **Aggregation & Sorting:** Finally, group the cleaned long-format data by `Region` and `Product_ID` (and keep the `Normalized_Name`, assuming a 1:1 mapping with `Product_ID`). Calculate the total sum of `Sales` (`Total_Sales`) and the mean of the interpolated `Temp` (`Avg_Temp`, rounded to 2 decimal places) for each group.
   
5. **Output Specification:** 
   Save the aggregated data to `/home/user/summary.csv`.
   The file must have exactly these columns in this order: `Region`, `Product_ID`, `Normalized_Name`, `Total_Sales`, `Avg_Temp`.
   Sort the final CSV primarily by `Region` (alphabetical A-Z) and secondarily by `Total_Sales` (descending, highest to lowest). If total sales are equal, sort by `Product_ID` ascending.

You may use any programming language (Python, R, bash tools, etc.) to accomplish this task. Ensure your final output matches the requested specification exactly.