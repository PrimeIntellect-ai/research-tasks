You are tasked with building a robust data validation script for our CSV processing pipeline. Recently, our data ingestion has been plagued by silent errors, such as integer IDs being implicitly converted to floats (e.g., `1001` becoming `1001.0` or `NaN`), numerical embeddings deviating from expected norms, and inactive users slipping into active datasets.

We have an image artifact at `/app/schema_guide.png` which contains a scan of the critical schema rules and reference values.

Your objective is to write a Bash shell script located exactly at `/home/user/filter_data.sh` that acts as a classifier and validator for incoming CSV files. 

Requirements for `/home/user/filter_data.sh`:
1. It must accept exactly one argument: the absolute path to a CSV file to evaluate.
2. It must read the target CSV, which has no header and the following format: `user_id,score,vector_x,vector_y`.
3. It must perform a multi-source data join against the master user database located at `/app/db/users.csv` (format: `user_id,status,join_date`) to retrieve the user's status.
4. It must enforce the strict schema rules extracted from `/app/schema_guide.png`. This includes strict integer validation (rejecting any decimals or missing values for IDs) and evaluating the vector data mathematically as specified in the image.
5. Exit codes: If the file perfectly conforms to all rules, the script must exit with code `0`. If the file violates ANY rule, it must exit with code `1`.
6. Use pure Bash, AWK, and standard GNU coreutils for the script implementation. Do not use Python or Pandas for the final script.

You should use `tesseract` to read the image at `/app/schema_guide.png` to understand the exact validation constraints you need to implement.