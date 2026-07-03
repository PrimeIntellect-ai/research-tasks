You are a log analyst investigating anomalous multi-language application behaviors. You have been provided with an archive of wide-format logs in `/home/user/raw_logs.zip`. Previous pipelines relying on simple shell tools have been silently dropping critical log events because some error messages contain embedded newline characters (`\n`). 

Your objective is to build a robust data processing pipeline using **Bash** and **Go** to correctly parse, reshape, normalize, and summarize these logs.

**Step 1: Orchestration Script**
Write a bash script `/home/user/pipeline.sh` that accepts a single argument (`extract`, `build`, `run`, or `all`) to orchestrate your pipeline as a simple DAG:
*   `extract`: Unzips `/home/user/raw_logs.zip` into `/home/user/raw_logs.csv`.
*   `build`: Compiles your Go program `/home/user/analyzer.go` into an executable `/home/user/analyzer`.
*   `run`: Executes the compiled `/home/user/analyzer`.
*   `all`: Runs `extract`, `build`, and `run` in the correct sequential order.

**Step 2: Go Data Processing**
Write the Go program `/home/user/analyzer.go`. When executed, it must read `/home/user/raw_logs.csv`.
The input CSV has the following wide-format header:
`EventID,Date,Node,Log_EN,Log_ZH,Log_RU`

Your Go program must perform the following:
1.  **Parsing:** Read the CSV. Ensure rows with embedded newlines in the quoted `Log_*` columns are parsed correctly without dropping any rows.
2.  **Reshaping (Wide to Long):** Convert the data into a long-format structure. For each wide row, emit a long row for every language column that is *not empty*.
    The long-format columns should be: `EventID,Date,Node,Language,Message`
    (Where `Language` is `EN`, `ZH`, or `RU`).
3.  **Unicode Normalization:** Before outputting, normalize every `Message` string to Unicode NFC (Normalization Form C) using Go's `golang.org/x/text/unicode/norm` package.
4.  **Output:** Write the resulting long-format data to `/home/user/reshaped_logs.csv` (include the header row). Embedded newlines must be preserved in the output CSV.

**Step 3: Templated Report Generation**
As part of the same Go program, analyze the long-format data to generate a summary report using Go's `text/template` package.
Write the report to `/home/user/report.txt` exactly matching this template format:

```
Total Events Processed: <count of original wide rows, excluding header>
Total Long Records: <count of non-empty language entries>
Multiline Messages: <count of long records where Message contains a newline character>
Node with most multiline messages: <Node name>
```
*Note: If there is a tie for the node with the most multiline messages, pick the one that appears first alphabetically.*

**Execution**
Once your code is written, run `./pipeline.sh all` to process the data and generate the final `reshaped_logs.csv` and `report.txt`. Ensure your scripts and code have the appropriate execute permissions.