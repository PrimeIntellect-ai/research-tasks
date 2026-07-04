You are an AI assistant helping a researcher organize their dataset metadata. 

The researcher has a SQLite database located at `/home/user/research_data.db` containing a hierarchical taxonomy of dataset categories and file metadata.

The database has two tables:
1. `categories`
   - `cat_id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
   - `parent_id` (INTEGER) - references `cat_id` (NULL for root categories)

2. `files`
   - `file_id` (INTEGER PRIMARY KEY)
   - `filename` (TEXT)
   - `size_bytes` (INTEGER)
   - `cat_id` (INTEGER) - references `categories.cat_id`

Your task is to write and execute a single SQLite query (via Bash `sqlite3` or a script) that calculates the **cumulative total size** of all files in each category. The cumulative size of a category must include the size of files directly in that category PLUS the sizes of all files in any of its descendant subcategories (to any depth).

After calculating the cumulative total sizes, rank the categories from largest total size to smallest.

Requirements for the output:
- Save the results to `/home/user/category_metrics.csv`.
- The output should be a strictly comma-separated CSV file (no headers, no spaces after commas).
- Columns should be: `category_name,cumulative_total_bytes,rank`
- Use the standard `RANK()` window function (order by `cumulative_total_bytes` descending) to determine the rank.
- Only include categories that have a cumulative size greater than 0.

Ensure your pipeline completes successfully and writes the exact requested format to the CSV file.