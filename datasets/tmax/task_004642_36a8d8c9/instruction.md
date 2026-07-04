You are a data analyst working with a custom dataset representing a small social network. The data is exported as CSV files located in `/app/data/`. 

You have been given an image file at `/app/query_spec.png` that contains the database schema and a specific natural language query request that your manager wants you to implement.

Your task is to:
1. Extract the schema and the query logic from the image `/app/query_spec.png` (you may use `tesseract` or any other tool).
2. Write a Python script at `/home/user/query.py` that takes exactly one command-line argument.
3. The script must process the CSV files in `/app/data/` to perform the graph traversal/join described in the image, using the command-line argument as the input parameter specified in the image.
4. The output must be printed to standard output exactly as requested in the image, with no extra text or logging.

The CSV files available in `/app/data/` are:
- `users.csv`
- `posts.csv`
- `tags.csv`
- `post_tags.csv`

Ensure your script is efficient enough to run quickly and handles the data correctly according to the schema shown in the image.