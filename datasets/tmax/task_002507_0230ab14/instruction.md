You are acting as a localization engineer working on a translation delivery network. We are experiencing sudden spikes in translation string requests for certain locales, which might indicate bot traffic or sudden virality. Your goal is to write a Bash-based data processing pipeline to detect these anomalies.

You are provided with a pre-vendored copy of GNU Datamash at `/app/datamash-1.20`. However, the source code contains a deliberate bug added by a previous engineer that prevents compilation. 

Your tasks:
1. Identify and fix the deliberate perturbation in `/app/datamash-1.20` (hint: check `src/datamash.c` for a compilation blocking error). 
2. Compile and build the package. You may place the resulting binary in `/home/user/.local/bin/` or use it directly from the build directory.
3. Write a Bash script at `/home/user/detect_anomalies.sh` that processes a CSV log file of translation requests. The script must accept the input CSV file path as its first argument and output the detected anomalies to standard output in CSV format.

Input CSV format (`timestamp,locale,string_id,access_count`):
```csv
timestamp,locale,string_id,access_count
1680307205,es-ES,ui_button_login,5
1680307210,es-ES,ui_label_welcome,2
1680308500,fr-FR,ui_button_login,1
...
```

The script must perform the following pipeline operations using `bash`, `awk`, `datamash`, or `sort`:
- **Normalization & Aggregation**: Convert the Unix `timestamp` to an integer hour (i.e., `floor(timestamp / 3600)`) to represent the "hour ID".
- **Stratification**: Group the data by `hour` and `locale`, and calculate the total `access_count` for each `locale` in each `hour`.
- **Rolling Statistics**: For each `locale`, order the data chronologically by `hour`. Compute a rolling average of the total `access_count` over the previous 3 hours (excluding the current hour). If there are fewer than 3 previous hours of data for a locale, use the available previous hours (if no previous hours exist, the rolling average is 0).
- **Anomaly Detection**: Flag an hour/locale combination as an anomaly if the actual total `access_count` for that hour is STRICTLY GREATER than `2.0 * rolling_average + 10`.

Output format (printed to standard output):
```csv
hour,locale,total_count,rolling_avg
466752,es-ES,150,45.33
466755,fr-FR,200,80.00
```
(Format rolling_avg to 2 decimal places. Do not include a header in the output).

Your script must run efficiently and correctly. An automated verifier will evaluate your script on a held-out test dataset, checking the F1 score of the detected anomalies against a known reference. You must achieve an F1 score of >= 0.90.