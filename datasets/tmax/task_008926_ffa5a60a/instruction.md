You are an AI assistant helping a data scientist clean a messy dataset using standard Linux command-line tools.

The user has a file located at `/home/user/patients.csv`. The file is supposed to have 5 columns separated by commas: `ID`, `Name`, `Email`, `SSN`, and `Notes`. 
However, some of the `Notes` fields contain embedded newlines without proper quoting, causing the rows to break across multiple lines. 

Your task is to write a short shell script or command pipeline to perform the following ETL (Extract, Transform, Load) operations:

1. **Clean**: Silently drop any lines in the file that do not contain exactly 4 commas. This will effectively remove the broken rows and their subsequent lines. Ignore the CSV header for the final output (do not include the header in the final JSON).
2. **Anonymize/Mask**: 
   - Mask the `SSN` field (column 4, original format `AAA-BB-CCCC`) so that only the last 4 digits are visible, replacing the rest with `X`s (e.g., `XXX-XX-CCCC`).
   - Extract only the domain name from the `Email` field (column 3). For example, `jane.doe@example.com` becomes `example.com`.
3. **Format & Template Generation**: Write the cleaned and masked data into a strictly formatted JSON file at `/home/user/report.json`. The JSON must match this exact structure:

```json
{
  "dataset": "patients",
  "valid_count": <number_of_valid_records>,
  "data": [
    {
      "id": "<ID>",
      "domain": "<email_domain>",
      "ssn": "<masked_ssn>"
    },
    ...
  ]
}
```

Make sure your JSON is valid (properly formatted with commas between array elements, but no trailing comma on the last element). You can use tools like `awk`, `sed`, `grep`, and `jq` to accomplish this. Do not write a separate Python script; stick to shell utilities.