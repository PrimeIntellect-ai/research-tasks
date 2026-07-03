You are tasked with investigating and fixing a severe memory leak in a long-running Python data processing service located at `/home/user/service`. 

The service processes streaming custom-encoded data, enriches it via a local SQLite database, and outputs transformed JSON. However, the process quickly consumes gigabytes of RAM and crashes out of memory. 

Your objectives are:
1. **Binary Reverse Engineering & Serialization Debugging**: The parsing logic is trapped inside a compiled Python bytecode file `/home/user/service/serializer.pyc`. There is no source code available. It is known to cache deserialized data improperly. You must analyze this bytecode (e.g., using Python's `dis` module or standard decompilation techniques), identify how it deserializes the payload, and recreate a fixed source file at `/home/user/service/serializer.py` that performs the exact same deserialization WITHOUT the unbounded caching mechanism. Delete the `.pyc` file once you have the `.py` replacement.
2. **Query Result Debugging**: The enrichment logic is in `/home/user/service/query_engine.py`. It currently pulls excessive amounts of data into memory when querying `/home/user/service/data/records.db`. Fix the SQL query in this file to fetch only the strictly required metadata for the requested `record_id`, filtering at the database level instead of in memory.
3. **Data Transformation Verification**: Run `python3 /home/user/service/main.py --run`. This will process the inputs and generate `/home/user/service/output.json`. Ensure that the transformed output perfectly matches the expected structure (the original service produced correct data, just inefficiently).
4. **Reporting**: Create a file at `/home/user/service/leak_report.txt` containing exactly two lines:
   - Line 1: The exact name of the global dictionary variable in the original `serializer.pyc` that caused the memory leak.
   - Line 2: The exact original flawed SQL query string from `query_engine.py` that fetched too much data.

Ensure all fixed files use efficient memory practices. The automated tests will check your `leak_report.txt`, the structural correctness of your rewritten `serializer.py`, the fixed `query_engine.py`, and the memory footprint of the running service.