You are a data engineer tasked with building the first stage of an ETL pipeline that extracts graph-like communication data from an undocumented SQLite database, computes a simple centrality metric, and outputs a validated JSON file.

An unknown colleague left an SQLite database at `/home/user/communications.db`. It contains information about users, message payloads, and how messages link users together (senders and receivers). 

Your tasks are:
1. Reverse engineer the schema of `/home/user/communications.db` to understand how users and message links are stored.
2. Write a Python script at `/home/user/etl_pipeline.py` that queries this database using complex joins to calculate the "communication score" for each user. A user's communication score is the total degree centrality in the message graph (i.e., the sum of messages they have sent AND messages they have received).
3. Filter the results to only include users with a communication score strictly greater than 2.
4. Sort the filtered users by their communication score in descending order. If there is a tie, sort alphabetically by username.
5. Paginate/limit the results to exactly the top 3 users.
6. Your Python script must validate the resulting data against the JSON schema located at `/home/user/schema.json` (you can use standard libraries, or install `jsonschema` if necessary) before writing to disk.
7. Save the final JSON array to `/home/user/top_users.json`.

The final output in `/home/user/top_users.json` must exactly match the schema defined in `/home/user/schema.json`.