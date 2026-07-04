I am a researcher organizing a massive multimodal astrophysics dataset. My data is currently split across two representations: 
1. A relational SQLite index located at `/home/user/data/catalog.db` with a table `Observations` (`id` TEXT PRIMARY KEY, `category` TEXT, `timestamp` TEXT).
2. A document-oriented storage directory at `/home/user/data/docs/` containing JSON files named `<id>.json` (e.g., `obs_001.json`).

I need you to build a local HTTP web service that allows me to query, merge, score, filter, and paginate this dataset. 

Requirements:
1. Bring up an HTTP service listening exactly on `127.0.0.1:8080`.
2. Implement a single endpoint: `POST /api/search`. 
3. The endpoint must require an authorization header: `X-Research-Token: astro-query-2024`. Return a 401 Unauthorized if missing or incorrect.
4. The request payload will be a JSON object specifying the query:
   `{"category": "<string>", "min_score": <float>, "page": <int>, "limit": <int>}`
   (Note: `page` is 1-indexed).

When a request is received, your service must do the following:
1. **Parameterized Query**: Query the SQLite database safely to retrieve all `id`s where `Observations.category` equals the requested category.
2. **Cross-representation Mapping**: For each retrieved `id`, load its corresponding JSON document from `/home/user/data/docs/<id>.json`.
3. **Merge**: Create a combined JSON object for each record in this exact format:
   `{"id": "<id>", "category": "<category>", "timestamp": "<timestamp>", "doc_data": <parsed_json_from_file>}`
4. **Scoring**: I have provided a proprietary, compiled legacy scoring engine at `/app/relevance_scorer`. It is a stripped binary. It takes a single JSON string (the merged object) as a command-line argument and prints a floating-point score to STDOUT. You must score every merged record.
5. **Filtering**: Discard any records where the calculated score is strictly less than `min_score`.
6. **Sorting**: Sort the remaining records in strictly descending order by their calculated score. If scores are tied, sort alphabetically by `id`.
7. **Pagination**: Apply the `page` and `limit` to the sorted, filtered list.
8. **Output Schema Validation**: The HTTP response must be a 200 OK with `Content-Type: application/json` returning exactly this validated schema:
   ```json
   {
     "page": <int>,
     "limit": <int>,
     "total_filtered_results": <int>,
     "results": [
       {
         "id": "<id>",
         "score": <float>,
         "merged_record": <the_merged_object>
       }
     ]
   }
   ```

You may use Python, Node.js, or bash to create this service. The service must stay running in the foreground once started, or you can start it in the background as long as it remains active for testing. Let me know when the service is up and running.