You are an ETL data engineer responsible for securing our data pipelines. We have a custom internal tool that generates complex SQL queries (including parameterized queries, complex joins, and window functions) from a JSON Domain Specific Language (DSL). 

First, our internal SQL generation package, `query-builder-1.0.0`, is located at `/app/vendored/query-builder-1.0.0`. However, the previous developer left a deliberate error in its `pyproject.toml` (a non-existent build dependency `fake-build-backend`), which prevents it from being installed. Fix the package perturbation and install it in your environment.

Second, we have been receiving malicious JSON ETL configurations from an untrusted source attempting SQL injection via table names, column names, and aliases (which cannot be parameterized easily). 

Your task is to write a Python script at `/home/user/sanitizer.py` that acts as a classifier. It must take a single command-line argument: the path to a JSON DSL file. 
The script must:
1. Parse the JSON DSL file.
2. Determine if it is malicious (contains SQL injection vectors like `;`, `--`, `DROP`, `UNION`, or unexpected SQL commands in fields that should just be identifiers).
3. Print exactly `SAFE` to stdout and exit with code 0 if the file is clean.
4. Print exactly `UNSAFE` to stdout and exit with code 1 if the file contains a SQL injection attempt or malicious payload.

To test your solution, we have provided two directories of JSON configs:
- `/app/corpora/clean/` : Valid, safe configurations that perform complex analytical aggregation and joins.
- `/app/corpora/evil/` : Configurations containing various SQL injection attacks in identifiers.

Your sanitizer must correctly classify 100% of the clean corpus as `SAFE` and 100% of the evil corpus as `UNSAFE`.