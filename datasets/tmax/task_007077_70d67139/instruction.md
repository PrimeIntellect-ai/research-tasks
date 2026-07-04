You are a Database Reliability Engineer. We have a backup of our microservice dependency graph stored in an SQLite database at `/home/user/services.db`. However, the schema documentation has been lost. 

Your task is to analyze this database and identify the most critical services to prioritize for our backup verification process. 

A service's "criticality" is determined by the total number of **unique** services that depend on it, either directly or indirectly (transitive dependents). 

Please perform the following steps:
1. Reverse engineer the data model of `/home/user/services.db` to understand how services and their dependencies are stored.
2. Formulate an index strategy and apply the necessary indexes to the database to optimize hierarchical querying.
3. Write a Python script at `/home/user/analyze.py` using the standard `sqlite3` library. The script should:
   - Use a single SQL query containing a recursive Common Table Expression (CTE) to calculate the number of unique transitive dependents for every service.
   - Use a Window Function to calculate the `DENSE_RANK` of each service based on its transitive dependent count (descending order).
   - Export the top 5 most critical services (ranks 1 to 5) to `/home/user/critical_services.csv`.

The output CSV `/home/user/critical_services.csv` must include headers and follow this exact format:
```csv
rank,service_id,service_name,dependent_count
1,4,auth_service,42
...
```

Do not use external Python libraries like `pandas` or `networkx`. All computation must be done within the SQLite engine using SQL.