You are a data analyst tasked with processing a messy dataset of multi-lingual user reviews. The dataset is provided as a CSV file at `/home/user/reviews.csv` with the following columns: `ReviewID`, `UserID`, `Language`, and `Text`.

You need to write a Go program (in `/home/user/process.go`) that reads this CSV, processes the data, and produces both a cleaned CSV file and a summary report. Your pipeline must accomplish the following:

1. **Unicode Normalization**: The `Text` field contains characters from multiple languages (English, Spanish, Japanese, Arabic, etc.) and is currently a mix of precomposed and decomposed Unicode characters. You must normalize the `Text` field of all rows to Unicode Normalization Form C (NFC).
2. **Anomaly Detection**: Flag a review as anomalous if the normalized `Text` contains the exact same character repeated consecutively 10 or more times (e.g., "aaaaaaaaaa" or "！！！！！！！！！！"). Anomalous reviews should be tracked but excluded from the final cleaned CSV.
3. **Deduplication**: Users sometimes submit the same review multiple times. If multiple rows have the exact same `UserID` AND the exact same normalized `Text`, keep only the first occurrence (lowest row index). Subsequent identical reviews by the same user are considered duplicates and should be excluded from the cleaned CSV. Do not consider a review a duplicate if the `UserID` is different. Anomaly detection takes precedence over deduplication (if an anomaly is duplicated, count the first as anomaly, and the second as duplicate).
4. **Clean CSV Generation**: Output the clean, normalized, non-anomalous, non-duplicate reviews to `/home/user/cleaned_reviews.csv` in the exact same format and column order as the input (`ReviewID,UserID,Language,Text`).
5. **Template-based Reporting**: Using Go's `text/template` package, read the template file located at `/home/user/report.tmpl` and generate a report file at `/home/user/report.md`. You must inject the exact counts of your processing.

The template file `/home/user/report.tmpl` looks exactly like this:
```markdown
# Review Processing Report
Total Reviews Parsed: {{.Total}}
Clean Reviews: {{.CleanCount}}
Anomalous Reviews: {{.AnomalyCount}}
Duplicates Removed: {{.DuplicateCount}}
```

**Constraints and Setup**:
- Initialize a Go module in `/home/user/processor` and write your code there.
- You may use external Go packages (e.g., `golang.org/x/text/unicode/norm` for NFC normalization).
- Ensure your output CSV includes the header row.
- Save the Go program as `/home/user/processor/process.go`, build it, and run it to produce the outputs.