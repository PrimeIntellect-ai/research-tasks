You are a web developer building a new lightweight analytics feature. To test the ingestion pipeline, you need to parse a batch of raw HTTP request logs, extract an encoded payload from the URL, decode it, and generate a summary CSV. 

Currently, `jq` is not installed on the system, and you don't have root access.

Please complete the following steps:
1. Create a directory `/home/user/bin`.
2. Download the official `jq` Linux 64-bit static binary (version 1.6) from `https://github.com/jqlang/jq/releases/download/jq-1.6/jq-linux64` and save it as `/home/user/bin/jq`. Make it executable.
3. Read the log file located at `/home/user/requests.log`.
4. Filter the log for `GET` requests where the path is exactly `/api/v1/event`. Ignore any other paths.
5. For the matching requests, extract the `data` query parameter from the URL.
6. The `data` parameter is a Base64-encoded JSON string. Decode it.
7. Use the `jq` binary you downloaded to parse the decoded JSON and extract the `userId` and `action` fields.
8. Output the results to `/home/user/processed_events.csv` with the header `userId,action` followed by the extracted values, separated by a comma.

Ensure the final CSV strictly follows this format:
```csv
userId,action
123,click
456,scroll
```

The task is complete when `/home/user/processed_events.csv` contains the correctly parsed and decoded data from the valid log entries.