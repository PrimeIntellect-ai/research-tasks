I need your help fixing a data retrieval script for my research datasets. 

I have a SQLite database located at `/home/user/research_data.db`. I was trying to write a query to aggregate measurements for specific researchers, but my script was returning wildly incorrect and duplicate results because of an implicit cross join, and I completely lost the original schema documentation. 

Fortunately, I found an old screenshot of the schema and business rules at `/app/schema_info.png`. 

Your task:
1. Use OCR (e.g., `tesseract`) to extract the schema details and business rules from `/app/schema_info.png`.
2. Reverse engineer the data model of `/home/user/research_data.db` using the extracted information. 
3. Write a Python script at `/home/user/fetch_data.py` that correctly queries the database without the cross-join bug.
4. The script must accept two command-line arguments: `--researcher` (a string) and `--min-val` (a float).
5. The script must output a strictly formatted JSON array of objects to standard output. Each object should have the exact keys: `experiment_name`, `measurement_date`, and `value`. 
6. The data must be filtered according to the business rules specified in the image.
7. Sort the JSON array by `measurement_date` ascending, then by `experiment_name` ascending.

Make sure your script uses parameterized queries to prevent SQL injection and properly handles the joins according to the image's instructions.