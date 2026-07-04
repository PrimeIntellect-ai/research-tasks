You are tasked with building a configuration state tracker in Rust that processes a large, streaming log of configuration changes, resamples them into fixed time intervals, and outputs the gap-filled state snapshots.

We have a system that logs every configuration variable change. However, downstream monitoring tools require a regular snapshot of the complete configuration state exactly every 1000 milliseconds.

You need to write a Rust program and a Makefile to orchestrate the pipeline.

**Requirements:**

1. **Rust Program (`/home/user/resampler.rs`)**:
    * Read an input CSV file containing configuration events. The file path should be provided as the first command-line argument.
    * The input CSV has the format: `timestamp_ms,key,value` (no header).
    * **Streaming:** The file might be very large, so you *must* read it line-by-line using a buffered reader (e.g., `BufReader`), rather than loading the entire file into memory at once.
    * **Resampling & Gap-filling:** Track the latest value for each `key`. You need to output a snapshot of the state at regular 1000 ms intervals. 
    * Let the first snapshot be at $T_0$, where $T_0$ is the smallest multiple of 1000 that is strictly greater than the first event's timestamp.
    * At each snapshot time $T$ (where $T = T_0, T_0 + 1000, T_0 + 2000, \dots$), output the state of all keys that have been seen up to (but *not* including) time $T$. If a key hasn't changed since the last snapshot, its previous value is carried forward (gap-filling).
    * Stop outputting snapshots when you reach a snapshot time $T$ that is strictly greater than the last event's timestamp.
    * Output format for each snapshot line: `T|key1:val1,key2:val2,...`
    * The keys in the output must be sorted alphabetically.
    * Print the output to `stdout`.

2. **Orchestration (`/home/user/Makefile`)**:
    * Write a Makefile with a default `run` target.
    * The `run` target should:
        1. Compile `resampler.rs` into an executable named `resampler` using `rustc`.
        2. Execute `./resampler /home/user/config_events.csv` and redirect the output to `/home/user/snapshots.log`.

**Input File Example (`/home/user/config_events.csv`):**
```
1000100,db_host,localhost
1000150,db_port,5432
1000500,db_host,db-primary
1001200,max_conns,100
1002050,db_port,5433
1003000,max_conns,200
```
*(In this example, the first event is at 1000100, so $T_0$ is 1001000. The last event is 1003000, so snapshots will be generated for 1001000, 1002000, 1003000, and 1004000).*

Please write the Rust program, write the Makefile, and execute `make run` to generate `/home/user/snapshots.log`.