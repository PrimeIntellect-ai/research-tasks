You are a localization engineer managing translation strings for a software application. You have two tab-separated values (TSV) files that need to be merged, cleaned, and analyzed to check for UI text expansion issues.

The files are:
1. `/home/user/base_en.tsv` - Contains the base English strings. Columns: `StringID`, `Category`, `EnglishText`.
2. `/home/user/trans_fr.tsv` - Contains the French translations. Columns: `StringID`, `TranslatedText`. Note that some translators accidentally left trailing or leading spaces in this file.

Your task is to process these files and generate a report at `/home/user/loc_report.tsv` using the following requirements:

1. **Join**: Merge the two files based on the `StringID`. Ensure the data is processed in ascending alphabetical order of `StringID`.
2. **Normalize**: 
   - Convert the `Category` column to strictly UPPERCASE.
   - Strip all leading and trailing whitespaces from the `TranslatedText` column.
3. **Rolling Statistic**: Calculate a rolling average of the character length of the *normalized* French `TranslatedText`. 
   - Use a window size of 3 (the current row and up to 2 previous rows). 
   - For the first row, it's just the length of its own text. For the second row, it's the average of the first two.
   - Format the rolling average to exactly 2 decimal places (e.g., `11.00`, `8.33`).

The final output file `/home/user/loc_report.tsv` must be a tab-separated file with exactly these 4 columns in this order:
`StringID` | `NormalizedCategory` | `NormalizedFrenchText` | `RollingAvgLen`

Do not include a header row in the output file. Use whatever tools you prefer (e.g., `awk`, `join`, `sort`, or a quick Python/Bash script).