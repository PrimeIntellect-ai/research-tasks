You are tasked with building a multi-stage time-series extraction and configuration tracking pipeline. A legacy configuration management system recently crashed, but we have a screen recording of its operational dashboard (`/app/dashboard.mp4`). To preserve data, the dashboard was configured to encode its raw event logs steganographically into the top-left pixel of the video feed.

Your goals are to:
1. Orchestrate a pipeline to extract the raw text logs from the video.
2. Build a robust Rust application that cleans, deduplicates, and tracks the state of the configuration over time.

### Part 1: Data Extraction Pipeline
The video `/app/dashboard.mp4` runs at exactly 10 frames per second. The single top-left pixel (x=0, y=0) of every frame contains 3 ASCII characters encoded in its 8-bit RGB channels (Red = 1st char, Green = 2nd char, Blue = 3rd char). 
You must write a shell script or pipeline (using `ffmpeg` and coreutils/scripting) to extract these pixels across all frames and concatenate the resulting characters into a raw text stream.

### Part 2: State Tracking Engine (Rust)
The raw text stream contains noisy configuration events. You must create a Rust CLI application at `/home/user/tracker` that reads these raw events from `stdin` and writes the normalized state time-series to `stdout`.

**Input Format (per line):**
`[TIMESTAMP] [OPERATION] [KEY] [VALUE]`
Example: `1620000000 SET database_url localhost`

**Processing Rules:**
1. **Cleaning:** Ignore any line that does not exactly match the 4-column space-separated format. The `TIMESTAMP` must be a valid `u64`. The `KEY` must contain only alphanumeric characters and underscores.
2. **Operations:**
   - `SET`: Creates a new key-value pair. If the key already exists, overwrite it.
   - `UPDATE`: Modifies an existing key. If the key does NOT currently exist in the state, ignore the command.
   - `DELETE`: Removes the key (the `[VALUE]` column will still contain a placeholder string, e.g., `NULL`, which should be ignored). If the key doesn't exist, ignore.
3. **Deduplication:** The raw log may contain duplicate events due to video encoding artifacts. If multiple valid events on the *exact same timestamp* affect the *exact same key*, only process the *last* valid operation for that key at that timestamp.
4. **State Emittance:** After processing all events for a given timestamp, if the configuration state has changed, output the entire state.

**Output Format:**
For every timestamp where the state changed (after processing all lines for that timestamp), output one line to `stdout`:
`<TIMESTAMP> => <KEY1>=<VAL1>, <KEY2>=<VAL2>, ...`
The keys must be sorted alphabetically. If the state becomes completely empty, output `<TIMESTAMP> => EMPTY`.

### Deliverables
1. A fully compiled release binary of your Rust tracker at `/home/user/tracker/target/release/config-tracker`.
2. Save the final processed state time-series of the video data to `/home/user/final_state.log` by running your extraction pipeline and piping it into your Rust binary.

*Note: Automated tests will programmatically fuzz your Rust binary against a strictly conforming oracle implementation with millions of edge-case inputs to verify bit-exact behavioral equivalence.*