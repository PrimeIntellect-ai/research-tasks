You are a data analyst tasked with processing a flight records CSV file.
A file located at `/home/user/flights.csv` contains data with the following columns: `id,source,dest,airline,delay`.

Write and execute a C program at `/home/user/process_flights.c` that does the following:
1. Reads `/home/user/flights.csv`.
2. Loads the data into an SQLite database (in-memory or on-disk). You may install `libsqlite3-dev` and include `<sqlite3.h>`.
3. Creates a composite index named `idx_airline_delay` on the table to optimize querying by `airline` and sorting by `delay`.
4. Queries the database for all flights operated by the airline `SkyCorp` that were delayed (`delay > 0`).
5. Sorts the results by `delay` in descending order, then applies pagination. Assuming a page size of 3 records, retrieve exactly "Page 2" (i.e., skip the first 3 records, and retrieve the next 3).
6. Exports these 3 records into a JSON file at `/home/user/page2.json`. The JSON must be an array of objects, with exactly this format (spacing does not strictly matter as long as it is valid JSON):
`[{"id": 8, "source": "MIA", "dest": "LAX", "delay": 60}, ...]`
7. Additionally, project the entire dataset of delayed (`delay > 0`) `SkyCorp` flights into a directed graph edge list. Export this to `/home/user/graph_edges.csv` with the header `source,dest,weight` where `weight` is the `delay`. Order the rows in this CSV by `weight` in descending order.

Requirements:
- Ensure your C program compiles with `gcc /home/user/process_flights.c -o /home/user/process_flights -lsqlite3`.
- Run your program so that `/home/user/page2.json` and `/home/user/graph_edges.csv` are generated correctly.