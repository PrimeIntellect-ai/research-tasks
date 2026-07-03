You are a data analyst troubleshooting an issue with a company's organizational chart. You requested a dump of the current employee-manager hierarchy from the HR SQLite database. However, due to a corrupted index returning stale rows, the database exported a raw, historical event log instead of the current active snapshot.

The exported file is located at `/home/user/org_events.csv`. 
It has the following header: `event_id,timestamp,employee,manager,event_type`

The `event_type` can be:
- `UPDATE`: Assigns or re-assigns the `employee` to a new `manager`.
- `DELETE`: The `employee` has left the company (their manager becomes irrelevant).

Because this is an event log, there may be multiple rows for the same employee over time. The rows are in chronological order (by `timestamp`). The *current* state of an employee is determined by their *latest* event. If their latest event is `DELETE`, they are no longer in the organization.

Your task is to:
1. Parse the CSV to determine the current, active manager for every employee.
2. Starting from the employee `EMP_404`, recursively traverse the hierarchy upwards to find their complete management chain.
3. The chain should end when it reaches `CEO`.
4. Export this management chain as a single comma-separated line to `/home/user/management_chain.txt`.

For example, if `EMP_404` reports to `EMP_22`, who reports to `EMP_1`, who reports to `CEO`, the output file should contain exactly:
`EMP_404,EMP_22,EMP_1,CEO`

You must accomplish this using only Bash, standard coreutils (like `sort`, `tail`), and text processing tools like `awk` or `sed`. Do not use Python, Perl, or other scripting languages.