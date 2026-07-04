You are tasked with fixing a data ingestion pipeline that processes video frame metadata. Our downstream regression models are failing because the previous pipeline silently converted invalid data into NaNs or Infs (similar to a pandas integer-to-float coercion bug), which poisoned our datasets. 

Your objectives are:

1. **Feature Extraction**:
   We have a raw video file at `/app/video/feed.mp4`. Extract the presentation timestamp (in seconds) and the packet size for every video frame using `ffprobe`. Save the output to `/home/user/extracted.csv`. The output must be a headerless CSV with two columns: `timestamp,size`. 
   *(Hint: use `-show_entries frame=pkt_pts_time,pkt_size -of csv=p=0`)*

2. **Strict Sanitization Filter (Go)**:
   Write a Go program at `/home/user/filter.go` that acts as a strict firewall for these CSV files. 
   The CLI usage must be:
   `go run /home/user/filter.go <input.csv> <output.csv>`
   
   The program must read the input CSV (two columns: timestamp, size) and perform the following checks:
   - Ensure both columns can be parsed as standard 64-bit floats.
   - **Crucial**: Reject any file (exit with status code `1`) if ANY row contains values that evaluate to `NaN`, `+Inf`, or `-Inf` in Go. Our downstream system crashes on these, even though Go's `strconv.ParseFloat` natively accepts the strings "NaN" and "Inf".
   - Reject the file (exit code `1`) if any `size` is negative.
   - If the file is perfectly clean, write the exact same rows to `<output.csv>` and exit with status code `0`.

3. **Validation**:
   You must ensure your Go script works flawlessly against our historical data corpora. 
   We have provided:
   - `/app/corpus/clean/`: Contains strictly valid CSVs. Your script must exit `0` for all of these.
   - `/app/corpus/evil/`: Contains adversarial CSVs with edge cases (e.g., injected "NaN", "infinity", out-of-bounds numbers). Your script must exit `1` for all of these.

4. **Integration**:
   Run your `filter.go` on your generated `/home/user/extracted.csv`, saving the result to `/home/user/clean_extracted.csv`.

Ensure your Go code is robust, strictly handles CSV parsing errors (rejecting the file if parsing fails), and explicitly checks for the silent NaN/Inf parsing behavior.