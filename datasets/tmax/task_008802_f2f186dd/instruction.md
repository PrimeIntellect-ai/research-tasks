You are helping a researcher organize their dataset of academic publications. They have stored their data in a SQLite database located at `/home/user/dataset.db` and wrote a C++ program at `/home/user/metrics.cpp` to analyze it.

The researcher wants to calculate a "Co-author Network Impact" metric for each author. Specifically, for each author, they want to find:
1. The number of unique co-authors they have worked with.
2. The total number of citations received by *all* papers written by those co-authors (including papers the original author wasn't on).

Unfortunately, the SQL query inside `metrics.cpp` contains an implicit cross-join bug (a missing join condition) that causes it to return incorrect, massively inflated results.

Your task:
1. Identify the schema of `/home/user/dataset.db`.
2. Fix the SQL query in `/home/user/metrics.cpp` to correctly compute the metrics without the cross join.
3. The C++ program should execute the query, sort the results by `CoAuthorTotalCitations` in descending order, then by `AuthorName` in ascending order, and apply pagination to only fetch the top 10 results.
4. The C++ program must write the results to `/home/user/top_coauthor_metrics.txt` in the exact format:
   `AuthorName|UniqueCoAuthorCount|CoAuthorTotalCitations`
   (One author per line).

You will need to compile the C++ code yourself (e.g., `g++ metrics.cpp -lsqlite3 -o metrics`) and run it to produce the final text file. Do not modify the database schema or data.