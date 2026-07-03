You are a localization engineer managing translation strings for multiple software projects. Every day, an automated system dumps the current total word counts for different projects in a "wide" CSV format. You need to create a Bash-based pipeline to process this data, reshape it, and calculate translation velocity metrics.

The input file is located at `/home/user/daily_loc_stats.csv` with the following header:
`Date,Project,EN,FR,ES`

Each row represents the total localized word count for a specific project on a specific date.

Your task is to write a script (using standard Linux utilities like `bash`, `awk`, `sed`, `sort`, etc.) that performs the following multi-stage pipeline:

1. **Wide-to-Long Reshaping:** Convert the data so each language (EN, FR, ES) has its own row, e.g., `Date, Project, Language, WordCount`.
2. **Aggregation:** Sum the `WordCount` across all projects for each `Date` and `Language` combination to get a total daily word count per language.
3. **Windowed Rolling Aggregation:** For each `Language`, calculate a 3-day rolling average of the total daily word count. 
    * The rolling average for a given date should include the sum of that date's total word count and the previous two available days' total word counts, divided by the number of days in that window (1, 2, or 3).
    * Round down (floor) the rolling average to the nearest integer.
4. **Output:** Save the final metrics to `/home/user/rolling_loc_stats.csv`.
    * The output file must include a header: `Date,Language,RollingAvgWords`.
    * The output rows must be sorted chronologically by `Date`, and then alphabetically by `Language`.

Requirements:
* The entire data processing must be written and executed in the terminal, utilizing Bash and core utilities.
* Do not use Python, Perl, or Ruby for the data transformation; rely on shell tools (e.g., `awk` is highly recommended).
* Ensure your final output exactly matches the requested CSV format and filename.