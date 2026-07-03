You are a localization engineer managing translation data updates. You have translation log files from multiple teams in different formats and need to align them to track translation velocity.

You have two data files:
1. `/home/user/loc_data/en_to_fr.csv` (Format: `Date,ID,Length`), where `Date` is an ISO8601 timestamp (e.g., `2023-10-01T10:00:00Z`).
2. `/home/user/loc_data/en_to_de.json` (Format: `[{"timestamp": <epoch_int>, "key": "<string>", "chars": <int>}, ...]`).

Your task is to build a multi-stage pipeline using C and a Makefile to process these files, align their timestamps to UNIX epoch time, merge them, and compute a rolling average of translation lengths.

### Requirements:

1. **Write a C program** at `/home/user/loc_processor.c`. It must support three sub-commands passed as the first argument:
   * `parse_csv <input_file> <locale>`: Reads the CSV file, parses the ISO8601 date to a UNIX epoch integer, and prints to stdout in TSV format: `<epoch>\t<locale>\t<ID>\t<Length>`. (Skip the CSV header).
   * `parse_json <input_file> <locale>`: Reads the JSON file and prints to stdout in the same TSV format: `<epoch>\t<locale>\t<key>\t<chars>`. You may write a simple string matching parser or use a lightweight library if you can install it without root.
   * `rolling_stats`: Reads the normalized TSV format from `stdin` (which will be sorted by epoch time). For each line, it computes a rolling average of the translation `Length` over a window of the **last 3 events** (including the current event). It must output the original line with the rolling average appended as a new column, formatted to 2 decimal places: `<epoch>\t<locale>\t<ID>\t<Length>\t<RollingAvg>`. If fewer than 3 events exist, it averages the available events.

2. **Write a Makefile** at `/home/user/Makefile` with the following targets:
   * `all`: Compiles `loc_processor.c` into an executable named `loc_processor`.
   * `pipeline`: This target must execute the full DAG:
     1. Run `./loc_processor parse_csv /home/user/loc_data/en_to_fr.csv fr` to generate `fr.tsv`.
     2. Run `./loc_processor parse_json /home/user/loc_data/en_to_de.json de` to generate `de.tsv`.
     3. Merge `fr.tsv` and `de.tsv`, sort them numerically by the first column (epoch time) in ascending order.
     4. Pipe the sorted output into `./loc_processor rolling_stats` and redirect the final output to `/home/user/final_stats.tsv`.

Ensure your C code compiles cleanly without errors. Run `make all` and then `make pipeline` so that `/home/user/final_stats.tsv` is generated.