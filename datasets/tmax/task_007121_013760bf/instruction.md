You are a localization engineer managing a time-series stream of translation updates from various global freelancers. You need to build a data processing pipeline in Bash to anonymize, sample, and log these translation events.

A raw time-series log of translation events has been exported to `/home/user/loc_events.tsv` (Tab-Separated Values).
The file has no header. The columns are:
1. `Timestamp` (ISO 8601, e.g., 2023-10-01T12:00:00Z)
2. `TranslatorEmail`
3. `LanguageCode` (e.g., AR, JA, RU, ES)
4. `TranslatedText` (UTF-8 strings)

Write a Bash script at `/home/user/process_loc.sh` that performs the following pipeline steps:

1. **Data Masking and Anonymization**: 
   Replace the `TranslatorEmail` with a masked version. The masking rule is: keep the first letter of the username, replace the rest of the username with a single asterisk `*`, and keep the `@domain.com` intact. 
   For example: `john.doe@example.com` becomes `j*@example.com`. `a@test.com` becomes `a*@test.com`.

2. **Time-Series Sorting and Stratified Sampling**:
   Sort all the records chronologically by the `Timestamp` (ascending). 
   Then, extract a stratified sample: output exactly the **first 2 chronological events** for each `LanguageCode`. If a language has fewer than 2 events, output all of them.

3. **Output**:
   Save the final processed, masked, and sampled TSV data to `/home/user/sampled_loc.tsv`. The output must be valid UTF-8 and retain the tab separation.

4. **Pipeline Logging and Monitoring**:
   Your script must generate a log file at `/home/user/pipeline.log`. The log must contain exactly these four lines (with real dynamic values for the counts):
   `[START] <Current_Timestamp_in_UTC>`
   `[PROCESSED] <Count_of_rows_in_input>`
   `[OUTPUT] <Count_of_rows_in_output>`
   `[END] <Current_Timestamp_in_UTC>`

Requirements:
- Ensure the script is executable (`chmod +x /home/user/process_loc.sh`).
- Use standard Bash utilities (awk, sed, sort, etc.). Python, Perl, or Ruby are not allowed for the main script.
- Execute the script once to generate the outputs before completing the task.