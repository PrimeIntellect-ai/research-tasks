You are a compliance officer performing an automated audit on your company's internal access management system. 

You have been provided with an SQLite database at `/home/user/audit.db`. This database logs access grants and revocations, as well as the hierarchical structure of company resources (roles, systems, and permissions). Due to a recent system glitch, some legacy query endpoints are returning "stale" access rows because they fail to account for the chronological order of events.

Your task is to calculate the **true** current access permissions and identify any employees who are in violation of a critical Separation of Duties (SoD) policy.

Here is the schema of `/home/user/audit.db`:

1. `access_events`
   - `event_id` (INTEGER PRIMARY KEY)
   - `employee_id` (TEXT)
   - `resource_id` (TEXT)
   - `action` (TEXT) - either 'GRANT' or 'REVOKE'
   - `timestamp` (INTEGER) - Unix epoch time of the event

2. `resource_hierarchy`
   - `parent_resource` (TEXT)
   - `child_resource` (TEXT)

**Rules for determining access:**
1. **Current Direct Access:** An employee currently has direct access to a `resource_id` if and only if the *most recent* (highest timestamp) event for that specific `(employee_id, resource_id)` pair has an `action` of 'GRANT'. If the most recent event is 'REVOKE', or if no events exist, they do not have direct access. (You will likely need window functions to determine this).
2. **Inherited Access (Graph):** Resources are hierarchical. If an employee has access (direct or inherited) to a `parent_resource`, they implicitly inherit access to all of its downstream `child_resource`s. You must map this out to the full transitive closure (e.g., if A->B and B->C, accessing A grants access to C).

**The Compliance Violation:**
An employee is in violation of the Separation of Duties policy if they have access (either directly or via inheritance) to BOTH of the following resources:
- `Vault_Open`
- `Vault_Close`

Write a Python script to query the database, process the hierarchical graph (you may use libraries like `networkx` or standard Python data structures), and find the violators.

**Output Requirement:**
Create a file at `/home/user/sod_violators.txt` containing the `employee_id`s of all employees who violate the SoD policy. Write one `employee_id` per line, sorted alphabetically.