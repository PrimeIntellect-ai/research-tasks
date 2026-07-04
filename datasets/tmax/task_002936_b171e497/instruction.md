You are assisting a corporate compliance officer auditing financial network databases for illicit structures.

Recently, the compliance team intercepted a handwritten memo containing a newly identified money-laundering topology. This memo has been scanned and saved to `/app/compliance_memo.png`.

Your task is to build a high-performance Python classifier that can audit a set of regional SQLite databases and flag those that contain the forbidden network topology described in the memo. 

Each region's database contains a corporate knowledge graph with two tables:
1. `entities` (`id` INTEGER PRIMARY KEY, `type` TEXT, `jurisdiction` TEXT)
    - `type` examples: 'PEP' (Politically Exposed Person), 'Shell', 'Corp', 'Individual'
    - `jurisdiction` examples: 'Standard', 'HighRisk'
2. `relations` (`source` INTEGER, `target` INTEGER, `rel_type` TEXT, `amount` REAL)
    - `rel_type` examples: 'owns', 'transfers_to'
    - `source` and `target` are foreign keys to `entities.id`.

**Instructions:**
1. Extract the compliance rule from the image at `/app/compliance_memo.png`. You may use `tesseract` to read it.
2. Write a Python script at `/home/user/audit_classifier.py` that takes a single command-line argument: the path to a directory containing SQLite databases (`.db` files).
3. The script must analyze every `.db` file in the provided directory using SQL. To match the forbidden topology efficiently, you must use complex joins and recursive Common Table Expressions (CTEs) up to the depth specified in the memo.
4. **Performance is critical.** The datasets can be large. Your script must dynamically design and apply an optimal index strategy (e.g., creating indexes on `relations` and `entities`) within the database connection before running the audit queries, or it will time out during the official test.
5. For each database in the directory, your script must output exactly one line to standard output in the following format:
   `[database_filename]: VIOLATION` (if the forbidden pattern exists)
   `[database_filename]: CLEAN` (if the forbidden pattern does not exist)

Example expected output for a directory containing `region_a.db` and `region_b.db`:
```
region_a.db: CLEAN
region_b.db: VIOLATION
```

Ensure your script is robust, properly parameterized, and exclusively prints the required audit results to standard output.