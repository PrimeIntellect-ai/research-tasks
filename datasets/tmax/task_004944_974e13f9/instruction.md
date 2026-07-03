You are a data analyst maintaining a NoSQL database system. We are auditing query logs stored in CSV format to prevent denial-of-service attacks caused by unbounded recursive graph traversals. 

Your objective is to write a C program that acts as a filter. It should read a CSV from standard input and write the valid rows to standard output. 

**Data Format:**
The incoming CSV data (without a header) has three columns, separated by commas:
`query_id,collection_name,pipeline_json`
(Note: You can assume the `pipeline_json` column contains no unescaped commas that would break a simple string split by the first two commas).

**Validation Rules:**
The `pipeline_json` column contains a serialized JSON array representing a NoSQL aggregation pipeline. 
You must validate this JSON. A row is considered **VALID** if:
1. It is valid JSON.
2. If any stage in the aggregation array contains a `"$graphLookup"` operation, the configuration object for that operation **MUST** contain a `"maxDepth"` key.
3. The `"maxDepth"` value must be an integer between `0` and `5` (inclusive). 
4. If `"maxDepth"` is missing, negative, or greater than 5, the entire row is **INVALID**.
5. Pipelines without `"$graphLookup"` are completely **VALID**.

**Your Program:**
* Must be written in C and saved at `/home/user/filter_pipelines.c`.
* Must output **only** the exact, unmodified lines of the CSV that are **VALID**.
* Must silently drop **INVALID** rows.
* You should compile it to `/home/user/filter_pipelines`.

**Dependencies:**
To parse the JSON, you must use the `cJSON` library. 
We have vendored the `cJSON` version 1.7.15 source code for you at `/app/cJSON-1.7.15/`. 
However, the previous maintainer made a mistake in the `Makefile` there, causing it to fail to compile. 
You must fix the `Makefile` in `/app/cJSON-1.7.15/`, compile the library, and link your `filter_pipelines.c` program against it.

Ensure your program handles standard input properly, as it will be tested against automated adversarial datasets containing both clean and malicious aggregation pipelines.