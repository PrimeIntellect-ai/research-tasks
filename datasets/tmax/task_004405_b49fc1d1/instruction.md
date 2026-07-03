You have been hired as a Database Reliability Engineer. Recently, our analytics database has been suffering from severe deadlocks and catastrophic performance degradation caused by rogue queries submitted by downstream analytical teams.

The Lead DBA has recorded a quick audio memo explaining the new query enforcement policies. You can find this memo at `/app/dba_notes.wav`. You will need to transcribe or listen to this audio (using tools available in your environment, such as `whisper` or `ffmpeg` combined with Python speech recognition) to understand the exact business rules, data model constraints, and index strategies required to stabilize the system.

Your task is to create a Python-based SQL query validator that enforces these rules. 

Requirements:
1. Write a Python script located exactly at `/home/user/query_validator.py`.
2. The script must accept a single command-line argument: the absolute path to a `.sql` file containing a single SQL statement or a block of SQL statements (like a transaction).
   Example invocation: `python3 /home/user/query_validator.py /path/to/query.sql`
3. The script must parse the SQL (you may install and use libraries like `sqlglot` or `sqlparse`) and check it against the DBA's rules specified in the audio file.
4. The script must output EXACTLY the word `ACCEPT` (if the query follows all rules) or `REJECT` (if the query violates one or more rules) to standard output. Do not print any other text, logs, or debugging information to stdout.
5. You must validate output schema and logic strictly. If a transaction has a high risk of deadlocking due to conflicting update orders, or if a window function is missing proper analytical aggregation boundaries, you must catch it.

To help you develop and test your script, a small set of sample queries has been provided in `/home/user/samples/`. However, your final script will be tested against a large, hidden adversarial corpus of "clean" and "evil" queries. To succeed, your validator must correctly reject 100% of the evil queries and preserve 100% of the clean queries.