You are assisting a researcher who is organizing a large collection of scientific datasets. 

The researcher has provided a SQLite database file at `/home/user/metadata.db`. This database contains hierarchical category information, dataset details, and author mappings, but the researcher has lost the exact schema diagram. 

Your task is to:
1. Analyze the schema of `/home/user/metadata.db` to understand how categories, datasets, and authors are related. Categories can have parent categories.
2. Write a recursive query to find all datasets that belong to the 'Genomics' category OR any of its subcategories (at any depth in the hierarchy).
3. Extract the title of these datasets and the names of their authors.
4. Export the results to a CSV file at `/home/user/genomics_datasets.csv`.

Requirements for the output CSV:
- It must have exactly two columns with headers: `title,author`
- It must be comma-separated.
- The rows must be sorted alphabetically by `title` in ascending order, and then by `author` in ascending order.
- You must use Bash and the `sqlite3` command-line tool to perform the extraction.