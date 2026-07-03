You are a data scientist working on an automated text processing pipeline. Your goal is to replace a legacy C-based data cleaning executable with a new, highly performant Go implementation, and properly integrate it into the local microservice architecture.

**Part 1: The Data Cleaner Implementation (Go)**
You need to write a Go program located at `/home/user/cleaner.go` and compile it to `/home/user/cleaner`.
This CLI tool must read a stream of CSV lines from STDIN and write JSON lines to STDOUT.
Input format: `id,review_text` (No header. `id` is a UUID or integer, `review_text` is arbitrary text).
Processing steps per line:
1. **Tokenization**: Convert `review_text` to lowercase. Remove all characters except alphanumeric (`a-z0-9`) and spaces. Split into tokens by continuous whitespace.
2. **Dimensionality Reduction (Feature Hashing)**: For each valid token (length > 0), compute the 32-bit FNV-1a hash of the token string. The feature bucket is `hash % 256`.
3. **Aggregation**: Count the frequency of each feature bucket for the given review.
4. **Output**: Print a JSON line: `{"id": "the-id", "features": {"bucket1": count1, "bucket2": count2}}`. (Omit buckets with 0 counts. Order of keys in the JSON object does not matter as long as it parses correctly).

There is an existing oracle binary at `/app/oracle_cleaner` that implements this exact logic. Your Go binary's input/output behavior must be **bit-for-bit identical** (semantically equivalent JSON, identical feature bucket calculations) to the oracle when tested with arbitrary text inputs.

**Part 2: Multi-Service Pipeline Configuration**
The data pipeline runs locally via a supervisor script at `/app/start_pipeline.sh`. It consists of 3 services:
- **`source-api`**: Serves raw CSV data on a local port.
- **`sink-api`**: An ingestion server that accepts POST requests with the cleaned JSON lines.
- **`processor-worker`**: A bash daemon that curls `source-api`, pipes the stream into your Go binary (`/home/user/cleaner`), and pipes the output to `sink-api`.

Currently, the pipeline is broken because the environment variables in `/app/pipeline.env` are misconfigured. 
1. Inspect the service scripts in `/app/services/` to determine the correct ports and URLs.
2. Update `/app/pipeline.env` so that `SOURCE_URL` and `SINK_URL` correctly point to the respective local service endpoints.
3. Ensure the `processor-worker` correctly invokes `/home/user/cleaner`.

Ensure your Go code is compiled and properly linked, and that `/app/pipeline.env` allows the end-to-end flow to succeed without errors when the supervisor script is executed.