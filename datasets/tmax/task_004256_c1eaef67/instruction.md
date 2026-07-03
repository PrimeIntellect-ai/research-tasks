You are a data scientist cleaning up an ETL pipeline that produced duplicate records on retry. Because of varying upstream sources, the duplicates have slight encoding differences, typos, and varying formats. 

You are given a dataset at `/home/user/input.csv` with the following columns: `name`, `email`, `address`.

Your task is to identify duplicate records and write the duplicate groups to `/home/user/duplicates.json`.

Two rows A and B are considered duplicates if they satisfy **Condition 1** OR **Condition 2**:

**Condition 1: Email Match**
Their normalized emails are strictly identical.
*Email Normalization:* Strip leading and trailing whitespace, then convert to lowercase.

**Condition 2: Name & Address Match**
Their normalized names have a Levenshtein distance of less than or equal to 2, **AND** their normalized addresses are strictly identical.
*Name Normalization:* Convert to Unicode NFC form.
*Address Normalization:* Convert to Unicode NFC form. Then, using regex, remove all characters except English letters and digits. Finally, convert to lowercase.

**Grouping:**
Duplicates are transitive. If A is a duplicate of B, and B is a duplicate of C, then A, B, and C all belong to the same group.

**Output Format:**
Create a JSON file at `/home/user/duplicates.json`.
The JSON should be an object where:
- The keys are the string representation of the lowest 0-based data row index in a duplicate group (row 0 is the first data row, skipping the CSV header).
- The values are sorted arrays of integers representing all row indices in that group (including the key itself).
- Only include groups that contain more than 1 record.

Example of expected output structure:
```json
{
  "0": [0, 5, 8],
  "2": [2, 3]
}
```

You may use any standard Python libraries or install packages via `pip` if needed (e.g. for calculating Levenshtein distance). Run your solution to produce the final `duplicates.json`.