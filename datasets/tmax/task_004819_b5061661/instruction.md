You are a data scientist tasked with cleaning and extracting features from a messy server log file.

The raw log file is located at `/home/user/raw_logs.txt`.

Each line in the log contains unstructured text representing user interactions. An example line looks like this:
`[INFO] 2023-10-01T12:00:01Z - User: U1234 performed Action: VIEW on Item: I987. Status: SUCCESS`

However, the file is messy:
- The casing for `User`, `Action`, `Item`, and `Status` values is inconsistent (e.g., `u1234`, `purCHASE`, `Success`).
- There are duplicate lines.
- Some actions failed (`Status: FAILED` or `Status: ERROR`), and we only care about successful ones.

Your task is to write a script in a language of your choice to process this file and compute user-level features. 

Here are the processing steps:
1. **Extraction**: Parse out the `timestamp`, `user_id` (the value after "User: "), `action` (the value after "Action: "), `item_id` (the value after "Item: ", ignoring the trailing period), and `status` (the value after "Status: ").
2. **Filtering**: Keep only records where the status is `SUCCESS` (case-insensitive).
3. **Normalization**: Convert all `user_id`, `action`, and `item_id` values to uppercase.
4. **Deduplication**: Remove any exact duplicate records. A record is an exact duplicate if it has the exact same `timestamp`, `user_id`, `action`, and `item_id` after normalization. Keep only one instance.
5. **Feature Extraction**: Group the cleaned records by `user_id` and calculate the following features for each user:
   - `total_actions`: The total number of successful, deduplicated actions performed by the user.
   - `unique_items`: The count of unique `item_id`s the user interacted with.
   - `most_frequent_action`: The `action` the user performed most frequently. If there is a tie for the most frequent action, choose the one that comes first alphabetically.

Output the results to a JSON file located at `/home/user/user_features.json`.
The JSON file should contain a single object where the keys are the normalized `user_id`s (sorted alphabetically), and the values are objects containing the three features exactly as named above.

Example expected output format:
```json
{
  "U001": {
    "total_actions": 2,
    "unique_items": 1,
    "most_frequent_action": "PURCHASE"
  },
  "U002": {
    "total_actions": 3,
    "unique_items": 2,
    "most_frequent_action": "VIEW"
  }
}
```