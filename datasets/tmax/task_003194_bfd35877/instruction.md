As a Database Reliability Engineer (DBRE), you are managing a cluster of read-only MongoDB backup nodes. Recently, developers have been submitting resource-intensive cross-query aggregations and unoptimized pipelines that cause the backup nodes to crash. 

To protect the infrastructure, you need to implement a Query Firewall in C that acts as a filter for incoming MongoDB queries and aggregation pipelines (represented as JSON). 

Additionally, we had a major crash last night. The automated root-cause analysis system generated a voice incident report at `/app/incident_report.wav`. You must transcribe this audio to find a specific database field that is currently causing out-of-memory errors when grouped by.

Your task:
1. Listen to or transcribe `/app/incident_report.wav` to identify the restricted field name.
2. Write a C program, `filter.c`, that reads a JSON payload (either a single JSON object for a query, or a JSON array for an aggregation pipeline) from standard input.
3. The C program must analyze the JSON and output exactly the string `EVIL` (and exit with code 1) if the query violates any of the following rules, or output `CLEAN` (and exit with code 0) if it is safe.
   
Rules for an EVIL query:
- Contains the `$where` operator anywhere in the JSON (preventing JavaScript execution).
- Contains the `$lookup` operator anywhere in the JSON (preventing cross-query joins on the backup node).
- Contains a `$group` stage where the `_id` field is exactly the restricted field name identified from the audio report (e.g., `{"$group": {"_id": "$RESTRICTED_FIELD", ...}}`).

To assist you, the `cJSON` library source files are provided in `/app/cjson/cJSON.h` and `/app/cjson/cJSON.c`. You may compile your program against them.

Compile your final executable to `/home/user/query_filter`.

We have provided a set of test queries in `/app/corpus/clean/` (which your filter must classify as CLEAN) and `/app/corpus/evil/` (which your filter must classify as EVIL). You can use these to test your implementation. Your filter must perfectly distinguish between the two corpora.