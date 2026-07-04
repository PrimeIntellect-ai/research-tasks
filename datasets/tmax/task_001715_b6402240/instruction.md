You are a data engineer responsible for optimizing and refactoring an old ETL pipeline. We have an undocumented SQLite database located at `/home/user/source.db` containing raw e-commerce data. Your predecessor left a system that is incredibly slow and hardcoded.

Your task has three phases:

**Phase 1: Dependency Installation & Data Model Reverse Engineering**
1. You must ensure `sqlite3` is installed on your system (install it using your package manager if necessary).
2. The database `/home/user/source.db` is completely undocumented and lacks indexes. Explore the database schema to understand the tables (there should be tables for customers, orders, and order items). Determine the relationships between them.

**Phase 2: Query Plan Optimization**
The current daily reporting query is too slow because it does full table scans. The goal of the query is to calculate the total amount spent by each customer on a specific `order_date`.
1. Analyze the tables and figure out which columns are used for joining and filtering.
2. Create a SQL script named `/home/user/optimize.sql` that contains `CREATE INDEX` statements to optimize joins and date filtering. The script must create at least three indexes to prevent full table scans when joining the tables and filtering by date. Apply this script to the database.

**Phase 3: Parameterized ETL Script**
1. Write a Bash script at `/home/user/etl.sh` that takes a single date argument in `YYYY-MM-DD` format (e.g., `./etl.sh 2023-10-15`).
2. The script must execute a single parameterized `sqlite3` query (using the CLI) against `/home/user/source.db` to extract the daily report.
3. The report must calculate the total spent per customer on the given date. Total spent is the sum of `quantity * unit_price` for all items in their orders on that date.
4. The script must output the results directly to a CSV file named `/home/user/report_<DATE>.csv` (e.g., `/home/user/report_2023-10-15.csv`).
5. The CSV must have exactly three columns in this order: `customer_id`, `customer_name`, `total_spent`. Format the `total_spent` to 2 decimal places. Order the CSV by `customer_id` in ascending order.
6. The CSV must include a header row.
7. Ensure your bash script is executable (`chmod +x`).

Constraints:
- Do not use Python, Perl, or other scripting languages. Use strictly Bash and the `sqlite3` CLI.
- Ensure that parameters are passed safely to `sqlite3` (do not just concatenate strings into the SQL query text).