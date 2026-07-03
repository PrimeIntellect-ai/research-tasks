I need you to act as a log analyst and help me correlate some disparate log files to find out which departments are generating the most system activity. 

I have two files in `/home/user/data/`:
1. `/home/user/data/activity.log`: A system log file containing unstructured text. Because it comes from a legacy Windows system, it is encoded in **UTF-16LE**.
2. `/home/user/data/users.csv`: A CSV file containing user identity mappings. It is encoded in **UTF-8**. It has a header row: `uuid,username,department`.

The `activity.log` contains lines that look like this:
`[INFO] 2023-10-25 10:15:30 User<123e4567-e89b-12d3-a456-426614174000> triggered action X`
Some lines might not contain a user action at all (e.g., system boot messages).

Your task is to write a Go program at `/home/user/analyze.go` that does the following:
1. Reads and decodes both files correctly.
2. Extracts the `uuid` from the `User<...>` pattern in the log file.
3. Joins the extracted UUIDs with the `users.csv` data to find the user's department.
4. Aggregates the total number of log events per department.
5. Writes the final aggregated statistics to `/home/user/department_stats.json`.

The output file `/home/user/department_stats.json` must be a flat JSON object where the keys are the department names (as strings) and the values are the total count of log entries associated with users in that department (as integers). Do not include any departments with 0 counts. If a UUID is found in the log but not in the CSV, ignore that log entry.

Example expected format for `/home/user/department_stats.json`:
```json
{
  "Engineering": 15,
  "Sales": 3,
  "HR": 1
}
```

Run your Go program to generate the JSON file. Let me know when you are done!