You are a data analyst tasked with debugging a daily reporting script. 

We have a Bash script located at `/home/user/report.sh` that processes two CSV files: `/home/user/users.csv` and `/home/user/purchases.csv`. The script converts these CSV files into JSON documents and then uses `jq` as an aggregation pipeline to compute the total spend per user.

However, the current script is producing wildly incorrect, inflated numbers. It appears the `jq` pipeline is performing an implicit "cross join" (Cartesian product) between the users and purchases, rather than matching them correctly by their IDs. Furthermore, the report is supposed to ONLY include users whose status is `"active"`, but the current script includes everyone.

Your task is to fix the `jq` aggregation pipeline inside `/home/user/report.sh` so that:
1. It correctly joins users and purchases on `user_id`.
2. It filters out any users who do not have a `status` of `"active"` (exclude inactive users completely, even if they have purchases).
3. It aggregates the data, calculating the sum of the `amount` field (as a number) for each active user.
4. The final output is written to `/home/user/summary.json` as a single JSON array of objects, sorted alphabetically by the user's `name`.

The output schema for `/home/user/summary.json` must strictly be an array of objects matching this structure exactly:
```json
[
  {
    "name": "Alice",
    "total_spent": 125
  },
  ...
]
```

Do not change the file paths or the names of the input/output files. Execute the script after fixing it to ensure `/home/user/summary.json` is generated correctly.