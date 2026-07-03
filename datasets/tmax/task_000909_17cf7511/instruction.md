You are an analyst managing a NoSQL database that also performs graph projections and analytical window functions. We have been experiencing performance issues and security leaks due to poorly constructed aggregation pipelines.

First, you will find an audio recording from our latest engineering briefing at `/app/meeting.wav`. Please transcribe this audio file. It contains the exact numeric `user_id`s that are strictly restricted and must never be queried or materialized.

Your task is to write a C++ query sanitizer.
1. Create a C++ source file at `/home/user/query_sanitizer.cpp` and compile it to `/home/user/query_sanitizer`. You may use standard libraries and lightweight single-header JSON libraries (like `nlohmann/json.hpp`, which you can download) if needed.
2. The executable must take a single command-line argument: the path to a JSON file containing a NoSQL aggregation pipeline (a JSON array of objects).
3. The program must evaluate the pipeline and print exactly `ACCEPT` or `REJECT` to standard output.

A pipeline MUST be `REJECT`ed if ANY of the following are true:
- Security Violation: It contains a `$match` stage that queries `user_id` for any of the restricted IDs mentioned in the audio (e.g., `{"$match": {"user_id": 42}}` or `{"$match": {"user_id": {"$in": [42, ...]}}}`).
- Security Violation: It contains a `$graphLookup` stage where `startWith` is one of the restricted IDs.
- Performance Violation: It contains a `$setWindowFields` stage (analytical aggregation) that is missing either the `partitionBy` field or the `sortBy` field. (Unbounded window functions cause memory exhaustion during graph materialization).

Otherwise, the pipeline MUST be `ACCEPT`ed.

You can test your program against the pre-existing corpora located at:
- `/app/corpus/clean/` (contains pipelines that should be ACCEPTed)
- `/app/corpus/evil/` (contains pipelines that should be REJECTed)

Write the C++ program, compile it, and ensure it correctly flags the corpora.