You are a Database Administrator optimizing a graph-like query for a NoSQL database (MongoDB). Your system tracks software packages and their dependencies. 

Currently, the application fetches dependencies iteratively, causing severe performance issues. You need to design a NoSQL aggregation pipeline using `$graphLookup`, define the appropriate index strategy to optimize it, and write a Python script to validate the output schema of the new query.

The `packages` collection contains documents like this:
```json
{
  "_id": "ObjectId(...)",
  "package_name": "web-server",
  "version": "1.2.0",
  "depends_on": ["http-lib", "auth-module"]
}
```

**Step 1: Aggregation Pipeline**
Create a file named `/home/user/pipeline.json` containing a valid JSON array representing the MongoDB aggregation pipeline. The pipeline must:
1. Start with a `$match` stage to find the package where `"package_name"` is `"gateway-api"`.
2. Use a `$graphLookup` stage to recursively find all transitive dependencies. 
   - Target the `packages` collection.
   - Start the recursion from the `depends_on` field.
   - Match the target documents on the `package_name` field.
   - Output the matched dependencies into a new array field called `transitive_dependencies`.
   - Limit the recursion depth to 5.

**Step 2: Index Strategy**
For the `$graphLookup` to be performant, the target collection requires a specific index. 
Create a file named `/home/user/index_strategy.json` containing a single JSON object representing the index key specification (e.g., `{"field_name": 1}`) that optimizes the `connectToField` lookup.

**Step 3: Output Schema Validation**
You have a mock output file at `/home/user/mock_output.json` and a JSON Schema at `/home/user/schema.json`.
Write a Python script at `/home/user/validate.py` that:
1. Loads both JSON files.
2. Uses the Python `jsonschema` library to validate the mock output against the schema.
3. If validation passes, writes the mock output identically to `/home/user/validated_output.json`.
4. If validation fails, it must catch the `jsonschema.exceptions.ValidationError` and write a JSON object `{"status": "invalid", "reason": "<error message>"}` to `/home/user/validated_output.json`.

Run your Python script to generate the final `/home/user/validated_output.json`.

*Note: Ensure all JSON files are properly formatted. You do not need a running MongoDB instance; just provide the correct JSON definitions and Python validation logic.*