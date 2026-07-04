You are a data engineer tasked with building an ETL pipeline that processes video telemetry and provides a query interface via parameterized MongoDB aggregation pipelines.

Your task has two phases:

**Phase 1: Video Telemetry Ingestion**
We have a dashboard recording video located at `/app/telemetry.mp4`. 
1. Ensure a local MongoDB instance is running (you may start it via standard background services or Docker if available, but assume the default port `27017` and no authentication).
2. Extract the coded picture number (`coded_picture_number`) and packet size (`pkt_size`) of all keyframes (I-frames) from the video. Use `ffprobe` to accurately retrieve this data.
3. Load this data into a MongoDB database named `etl`, in a collection named `iframes`. Each document must have the exact structure: `{"frame_idx": <int>, "pkt_size": <int>}`. 

**Phase 2: Parameterized Query Construction**
You must write a Python script at `/home/user/build_query.py` that takes a single JSON string as a command-line argument and outputs the result of a MongoDB aggregation pipeline to `stdout`.

The input JSON will have the following structure:
`{"min_size": <int>, "max_size": <int>, "limit": <int>, "sort_order": <1 or -1>}`

Your script must:
1. Connect to the local MongoDB `etl.iframes` collection.
2. Construct a parameterized NoSQL aggregation pipeline that performs the following exact sequence of stages:
   - A `$match` stage that filters documents where `pkt_size` is between `min_size` and `max_size` (inclusive on both ends).
   - A `$sort` stage that orders the results by `pkt_size` using the provided `sort_order` (1 for ascending, -1 for descending). If there is a tie, secondary sort by `frame_idx` ascending.
   - A `$limit` stage that restricts the number of processed documents to `limit`.
   - A `$group` stage that groups all remaining documents together (`_id: null`), calculates the `$avg` of their `pkt_size` (stored in field `average_size`), and accumulates their `frame_idx` into an array (stored in field `frames`).
   - A `$project` stage that excludes the `_id` field.
3. Execute the pipeline.
4. Print the exact output array as a compact JSON string (no spaces, using `json.dumps(list(cursor), separators=(',', ':'))`).

Ensure your script handles edge cases gracefully (e.g., empty results should print `[]`). Make sure the script is executable and relies solely on standard Python libraries plus `pymongo`.

We will verify your solution by feeding hundreds of randomly generated query parameters to your script and comparing the bit-exact output against a known verified oracle.