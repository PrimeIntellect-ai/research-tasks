You are a data engineer building an ETL pipeline to process distributed retail sales data. 

The raw data is stored in a nested directory structure under `/home/user/raw_data/`. The directory contains multiple CSV files representing daily sales from different regions and stores (e.g., `/home/user/raw_data/region_north/store_12/sales_20231001.csv`).

Every CSV file has a header line and follows this exact format:
`transaction_id,item_category,quantity,unit_price,discount_percentage`

Your task is to build a shell-based data transformation pipeline that accomplishes the following:

1. **Analysis Environment Setup:**
   Create an output directory at `/home/user/etl_output/` and an archive directory at `/home/user/archive/`.

2. **Tabular Data Transformation and Aggregation (Mathematical):**
   Process all CSV files in the `raw_data` directory (excluding the header lines).
   For each transaction, calculate:
   - `Gross Revenue = quantity * unit_price`
   - `Discount Amount = Gross Revenue * (discount_percentage / 100)`
   - `Net Revenue = Gross Revenue - Discount Amount`
   
   Aggregate the total `Net Revenue` and total `Discount Amount` per `item_category`.

3. **Output Formatting:**
   Save the aggregated results to `/home/user/etl_output/category_summary.tsv`.
   The output must be a Tab-Separated Values (TSV) file with no header.
   Each line must follow this format:
   `item_category<TAB>total_net_revenue<TAB>total_discount_amount`
   Round the numeric values to exactly two decimal places (e.g., `145.50`).
   Sort the final output file alphabetically by `item_category`.

4. **Storage Management:**
   Once the aggregation is complete, package the entire `/home/user/raw_data/` directory into a compressed tarball at `/home/user/archive/raw_data_backup.tar.gz`.
   After verifying the tarball is created, delete the original `/home/user/raw_data/` directory to free up storage space.

You must accomplish this using standard Linux command-line tools (`awk`, `find`, `tar`, `sort`, etc.). Do not write standalone Python/Ruby scripts.