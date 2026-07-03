You are a data engineer tasked with building an ETL pipeline to detect anomalies in a multilingual event stream. 

You have been provided a dataset at `/home/user/events.csv` containing timestamped text events. The file has the following header: `timestamp_sec,language,content`.

Your task is to write a Go program (`/home/user/etl.go`) that performs the following data processing steps:

**1. Anomaly & Changepoint Detection:**
- Group the events by their `timestamp_sec`.
- Calculate the total number of events that occurred in each second.
- Define an **"anomaly second"** as any second where:
  a) The total number of events is strictly greater than 5.
  b) The total number of events is at least exactly double (>= 2.0x) the number of events in the *immediately preceding* second (i.e., `T - 1`). If `T - 1` has no events recorded, treat its count as 0 (any count > 5 is an anomaly since it's >= 2 * 0).

**2. Unicode Processing & Stratified Sampling:**
- Collect all individual events that occurred during *any* of the identified "anomaly seconds".
- Stratify these anomalous events by their `language`.
- For each language, sample exactly the top 2 events based on the length of their `content` measured in **Unicode runes** (descending). 
- If events have the same rune length, break ties by sorting the `content` lexicographically (ascending, standard string comparison). If there is still a tie, keep both (or either, since the content is identical). If a language has fewer than 2 events, include all of them.

**3. Output Generation:**
- Write the final stratified sample to `/home/user/anomalies_sampled.json`.
- The output must be a JSON array of objects, with each object structured exactly like this:
  `{"timestamp_sec": 102, "language": "en", "content": "Sample text"}`
- The JSON array must be sorted by `language` (ascending), then by content rune length (descending), then by `content` (ascending).

**Requirements:**
- Write and execute the Go code to process the data.
- You may use any standard Go libraries.
- Ensure your code is compiled and run to produce the output file `/home/user/anomalies_sampled.json`.