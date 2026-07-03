You are a data analyst. You have been provided with an archive of raw CSV files in `/home/user/data/` that were exported from an undocumented legacy system. 

The directory `/home/user/data/` contains four files:
1. `clients.csv`
2. `items.csv`
3. `purchases.csv`
4. `purchase_lines.csv`

The system's documentation was lost, so column names are inconsistent (e.g., primary keys might be `id`, `client_id`, `item_code`, while foreign keys might be `c_ref`, `item_ref`, `p_id`, etc.). 

Your objectives are:
1. **Reverse Engineer & Build Database**: Write a Python script `/home/user/build_db.py` that reads these CSV files, infers their relationships based on column names and data types, and loads them into a new SQLite database at `/home/user/store.db`. The tables must be named `clients`, `items`, `purchases`, and `purchase_lines`. You must explicitly define Primary Keys and Foreign Keys in your `CREATE TABLE` statements within the Python script.
2. **Design Index Strategy**: To optimize analytical queries, design appropriate database indexes based on the inferred foreign key relationships and common filtering columns. Write the SQL statements to create these indexes and save them to `/home/user/indexes.sql`. Execute these statements against the database.
3. **Query Construction**: Write a SQL query that calculates the total amount spent specifically on items in the "Electronics" category for each client. The output should include the client's name and their total amount spent, ordered from highest spender to lowest spender. Save this SQL query in `/home/user/query.sql`.
4. **Export Results**: Execute your query and save the top 3 results to a CSV file at `/home/user/top_spenders.csv`. The CSV must have exactly two columns with the headers: `client_name,total_spent`.

Ensure all requested files (`build_db.py`, `store.db`, `indexes.sql`, `query.sql`, `top_spenders.csv`) are created in `/home/user/`. Use only standard Python libraries (like `sqlite3` and `csv`).