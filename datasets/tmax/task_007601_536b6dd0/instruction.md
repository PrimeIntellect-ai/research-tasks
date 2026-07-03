I am building an ETL pipeline to clean and select features from my system metrics dataset, but my current analysis setup is broken and generating blank models. I need you to build a reliable Go tool to process the raw data.

The raw dataset will be located at `/home/user/raw_data.csv`. It contains numeric system metrics but has some rows with missing values labeled as "NA". 

Please write a Go program at `/home/user/etl.go` that performs the following steps:
1. **ETL Pipeline Setup**: Read `/home/user/raw_data.csv`.
2. **Data Cleaning**: Remove any entire row that contains the string "NA" or an empty field in any column.
3. **Correlation Analysis**: For the remaining clean rows, calculate the Pearson correlation coefficient between all pairs of numeric columns.
4. **Feature Selection**: Scan the columns from left to right (index 0 to N-1). If any column has an absolute Pearson correlation strictly greater than `0.85` with a column that appeared *earlier* (to its left), that column must be dropped to remove redundant features.
5. **Output**: Write the remaining rows and columns to `/home/user/clean_data.csv`, preserving the original header names for the kept columns. Format all numeric outputs to exactly one decimal place (e.g., `1.0`).

Once you have written the Go script, compile and run it so that `/home/user/clean_data.csv` is produced. Do not use any external Go libraries outside of the standard library.