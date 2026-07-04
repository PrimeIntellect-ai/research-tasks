You are tasked with building a highly efficient configuration change tracker in C. 

A fleet of servers periodically sends their current configuration states. These states are logged sequentially in a massive CSV file at `/home/user/config_stream.csv`. The file format is:
`Timestamp,ServerID,ConfigKey,ConfigValue`

Most of the time, the configuration hasn't changed from the previous report. Your goal is to extract only the actual *changes* (state transitions) and generate an HTML report using a streaming approach.

**Requirements:**
1. **C Program:** Write a C program at `/home/user/tracker.c` and compile it to `/home/user/tracker`.
2. **Streaming & Hash-based Deduplication:** The program must read `config_stream.csv` line-by-line. To minimize memory usage, you **must not** store the raw `ConfigValue` strings in memory to track state. Instead, use a hash table that keys on `ServerID_ConfigKey` and stores only a 32-bit or 64-bit integer hash (e.g., djb2 or FNV-1a) of the latest `ConfigValue`.
3. **Change Detection:** A configuration is considered "changed" if it's the first time the `ServerID` + `ConfigKey` is seen, OR if the hash of its `ConfigValue` differs from the currently stored hash for that combination.
4. **Template-based Generation:** For every detected change, your C program must output an HTML block to `/home/user/report.html`. The output file must consist *only* of these concatenated blocks (no `<html>` or `<body>` wrappers needed). The format for each change must be exactly:
```html
<div class="change">
  <span class="time">{Timestamp}</span>
  <span class="server">{ServerID}</span>
  <span class="key">{ConfigKey}</span>
  <span class="value">{ConfigValue}</span>
</div>
```
*(Replace `{Timestamp}`, `{ServerID}`, `{ConfigKey}`, and `{ConfigValue}` with the actual extracted values from the CSV line. Do not include the curly braces. Maintain the exact whitespace and indentation shown above.)*

Ensure your C program is compiled and executed to produce `/home/user/report.html`.