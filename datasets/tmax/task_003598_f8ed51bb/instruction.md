Wake up! It's 3:00 AM and you've just been paged. The critical `trace_aggregator` service has crashed in production, halting our observability pipeline. 

The service is written in Rust and is located at `/home/user/trace_aggregator`. It reads a unified stream of JSON log events from `/home/user/logs/combined.jsonl`, aggregates the start and end times of distributed traces across multiple services, and outputs a summary to `/home/user/completed_traces.json`.

Initial triage shows that the program panics with an `unwrap()` error. The system administrator noticed that there was a recent network partition between Service B and Service C, causing some log events to be written out of chronological order. 

Your tasks are:
1. Examine the source code in `/home/user/trace_aggregator/src/main.rs` to understand how events are parsed and state is traced.
2. Reconstruct the timeline of events from `/home/user/logs/combined.jsonl` to identify exactly which `trace_id` and event sequence is causing the crash.
3. Fix the Rust code so that it gracefully handles "END" events that arrive before (or without) their corresponding "START" events. If an "END" event has no corresponding "START" in the active traces map, the program should simply ignore it and continue processing the rest of the file without panicking.
4. Compile and run your fixed program. 
5. Write the resulting aggregated output to `/home/user/completed_traces.json` (the application should already do this once the panic is fixed, but verify it is created successfully).
6. Create a text file at `/home/user/root_cause.txt` containing the exact `trace_id` that triggered the original panic.

Work fast, the pipeline is backing up!