You are a data engineer troubleshooting a broken ETL pipeline. 

You have been given two files in your home directory:
1. `/home/user/raw_events.json`: A JSON array of raw event logs from our web application. Each event has an `event_type` and a `u_id`.
2. `/home/user/warehouse.sqlite`: An undocumented SQLite database containing our dimension tables. 

Your task is to generate a summary report of purchases by user group.

Requirements:
1. Reverse engineer the schema of `/home/user/warehouse.sqlite` to find the tables containing user IDs, their associated group codes, and the human-readable group names. 
2. Filter `/home/user/raw_events.json` to extract only events where `event_type` is exactly `"purchase"`.
3. Perform cross-data-source aggregation: Calculate the total number of "purchase" events for each human-readable group name.
4. Output the result to exactly `/home/user/purchase_summary.json`.

Output Schema Validation:
The file `/home/user/purchase_summary.json` MUST strictly be a JSON array of objects with exact keys `group_name` (string) and `purchase_count` (integer). 
The array must be sorted by `purchase_count` in descending order. If there is a tie, sort by `group_name` in alphabetical order.

Example valid output format:
```json
[
  {
    "group_name": "Early Adopters",
    "purchase_count": 42
  },
  {
    "group_name": "Beta Testers",
    "purchase_count": 15
  }
]
```

Do not include any groups that have 0 purchases.