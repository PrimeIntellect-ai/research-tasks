You are a data engineer building a high-performance ETL pipeline. A critical step in this pipeline involves extracting relational data from a SQLite database, transforming it into a document-oriented JSON format, and supporting pagination for downstream batch processing. For performance reasons, this extraction tool must be written in C.

A SQLite database is located at `/home/user/warehouse.db`. It contains three tables representing an article publishing platform:

1. `authors`
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
   - `reputation` (INTEGER)

2. `articles`
   - `id` (INTEGER PRIMARY KEY)
   - `author_id` (INTEGER, foreign key to authors.id)
   - `title` (TEXT)
   - `views` (INTEGER)

3. `tags`
   - `article_id` (INTEGER, foreign key to articles.id)
   - `tag_name` (TEXT)

Your task is to write a C program at `/home/user/etl_extract.c` that connects to `/home/user/warehouse.db` and performs the following operations:

1. **Schema Analysis & Complex Joins**: Query the database to find all articles that have the tag exactly matching `"AI"` AND whose author has a `reputation` strictly greater than `100`.
2. **Result Sorting & Pagination**: Sort the resulting articles by `views` in strictly DESCENDING order. The program must accept exactly two command-line arguments for pagination: `<limit>` and `<offset>` (in that order). These should be applied to the query.
3. **Cross-Representation Mapping**: Transform the SQL result set into a JSON array of objects. Each object must have the following exact keys and types:
   - `"article_id"` (integer)
   - `"title"` (string)
   - `"author_name"` (string)
   - `"views"` (integer)

The C program must output this JSON array directly to a file named `/home/user/output.json`. Do not output anything to standard output. 

**Requirements:**
- The program must be compiled to `/home/user/etl_extract`. You will need to link the SQLite3 library (e.g., `gcc -o etl_extract etl_extract.c -lsqlite3`).
- You must manually construct the JSON string in C (do not use external JSON libraries like jansson or cJSON, keep it dependency-free aside from standard library and sqlite3).
- Once compiled, execute your program with a limit of `3` and an offset of `1`:
  `/home/user/etl_extract 3 1`

Ensure your code safely handles basic SQL errors and safely escapes quotes in titles if necessary (though for this dataset, you may assume titles are alphanumeric with spaces).