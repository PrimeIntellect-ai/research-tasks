You are tasked with recovering an event sequence from a corrupted data export and building a reliable query interface for it.

We have a corrupted CSV file located at `/app/data/export.csv` containing hierarchical event logs. Unfortunately, the system that exported this data had a corrupted index, resulting in duplicated, stale, and out-of-order rows. 

To help reconstruct the correct state, we captured a video of the legacy system's transaction dashboard rendering the correct sequence of event IDs over time, located at `/app/reference_video.mp4`. 

Your task consists of three parts:
1. Extract the valid sequence of Event IDs from the video. You will need to process `/app/reference_video.mp4` (ffmpeg and tesseract-ocr are installed) to extract the event IDs that flash on the screen.
2. Filter the `/app/data/export.csv` to only include the rows corresponding to the valid sequence of Event IDs, deduplicating any stale rows by taking the one with the latest `timestamp` for each ID.
3. Write a Go program at `/home/user/query_engine.go` that loads this cleaned dataset and implements a specific command-line query interface.

The Go program must accept exactly one argument: a JSON string containing an array of query objects. It should output a JSON array of results to standard output.

Query object format:
```json
{
  "type": "ancestors",
  "event_id": "12345",
  "limit": 10,
  "sort": "desc"
}
```

The CSV has the following columns: `event_id`, `parent_event_id`, `timestamp`, `event_type`, `payload`.

For the "ancestors" query, your Go program must return all ancestors of the given `event_id` up to the root, sorted by timestamp (ascending or descending as specified), limited by the `limit` parameter. The output for each query should be an array of `event_id` strings.

Your Go program will be tested extensively against a reference implementation with thousands of randomized inputs to ensure perfect equivalence. Ensure your recursive querying and output schema validation are perfectly robust.