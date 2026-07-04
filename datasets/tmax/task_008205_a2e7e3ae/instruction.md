You are a data scientist working with a messy dataset of product reviews. The data engineering team exported a JSON-lines file, but a bug in their exporter caused Unicode characters in the `review_text` field to be double-escaped (e.g., the string contains literal characters `\` `u` `0` `0` `e` `9` instead of the actual character `é`). 

Your task is to build a Rust pipeline to clean this data, bulk-export it into a SQLite database, and generate a summary report.

Specifically, you need to:
1. Create a Rust project (using Cargo) in `/home/user/review_cleaner`.
2. Write a Rust program that reads `/home/user/raw_data.jsonl`. Each line is a JSON object with the following string fields: `id`, `category`, `product_name`, and `review_text`.
3. For each record, fix the `review_text` field by unescaping any double-escaped Unicode sequences (i.e., convert literal `\uXXXX` sequences back into their proper UTF-8 characters).
4. Group the cleaned records by `category`.
5. The Rust program must output two files:
   - `/home/user/insert.sql`: A SQL script that first creates a table `reviews (id TEXT, category TEXT, product_name TEXT, review_text TEXT)` and then inserts all the cleaned records using standard `INSERT INTO reviews VALUES ...` statements.
   - `/home/user/report.md`: A template-based summary report of the counts per category. The categories must be sorted alphabetically. The format must exactly match:
     ```
     # Category Report
     - [Category Name]: [Count] reviews
     ```
     (e.g., `- electronics: 5 reviews`)
6. Finally, execute the generated `/home/user/insert.sql` against a new SQLite database located at `/home/user/reviews.db` using the `sqlite3` CLI tool.

Constraints:
- You may use standard Rust crates (like `serde`, `serde_json`, `regex`) by adding them to your `Cargo.toml`.
- Do not use a Rust SQLite driver to do the insertion directly; you *must* generate the `insert.sql` file and use the `sqlite3` command-line tool.