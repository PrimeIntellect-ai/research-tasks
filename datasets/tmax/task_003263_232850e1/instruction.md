You are a data engineer debugging an ETL pipeline written in Bash. We have a legacy shell script `/home/user/etl_pipeline.sh` that extracts data from a SQLite database (`/home/user/data.db`) and enriches it with document data from a JSON file (`/home/user/segments.json`).

The script is currently producing incorrect results (way too many rows) due to an implicit cross join in its SQL query. It is also poorly optimized.

Your task:
1. Reverse engineer the data model by inspecting `/home/user/data.db` and `/home/user/segments.json`.
2. Fix the SQL query inside `/home/user/etl_pipeline.sh` so that it correctly joins the database tables without causing a Cartesian product.
3. Ensure the bash script correctly maps the extracted relational data with the document data (JSON) based on `segment_id`.
4. The final output must be saved to `/home/user/report.csv` containing precisely these comma-separated columns: `order_id,user_name,segment_name,amount`.
5. The records in `/home/user/report.csv` must be sorted by `order_id` in ascending order.
6. Do not include a header row in the final CSV.

You can run the script using `bash /home/user/etl_pipeline.sh`. Make sure you modify the script so that running it directly generates the correct `/home/user/report.csv`.