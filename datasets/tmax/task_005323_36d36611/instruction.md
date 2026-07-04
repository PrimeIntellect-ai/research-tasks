You are assisting a compliance officer who is auditing our internal systems for unauthorized access anomalies. 

We have a local MongoDB instance running (or you need to set one up locally) containing an access log. The log data is stored in a MongoDB collection called `access_logs` within the `compliance` database. 

Your task is to write a Go program (`/home/user/audit.go`) that connects to this database and performs the following operations:

1. **Database Setup**: We have a setup script at `/home/user/setup_env.sh` which will download MongoDB, start it on `localhost:27017`, and populate the `compliance.access_logs` collection. Run this script first.
2. **Query Optimization**: Modify the Go program to create an index on the `role` and `endpoint` fields to ensure the upcoming query runs efficiently.
3. **NoSQL Aggregation Pipeline**: Construct a MongoDB aggregation pipeline to find anomalous access patterns. Specifically, find all users with the `role` equal to `"guest"` who have accessed endpoints starting with `/api/admin/`. Group the results by `user_id` and count the number of *total* accesses. Only include users who have accessed an admin endpoint 3 or more times.
4. **Query Plan Interpretation**: Your Go program must use the MongoDB `explain` command (or explain method on the aggregate) to retrieve the query execution plan for your aggregation pipeline. Save the raw JSON output of this plan to `/home/user/query_plan.json`.
5. **Output Schema Validation**: Read the results of the aggregation. Validate that the output strictly matches this Go struct:
   ```go
   type AuditResult struct {
       UserID string `json:"user_id" bson:"_id"`
       TotalAccesses int `json:"total_accesses" bson:"total_accesses"`
   }
   ```
6. **Result Output**: Save the JSON-encoded list of `AuditResult` objects to `/home/user/audit_results.json`.

Compile and run your Go program to produce `/home/user/audit_results.json` and `/home/user/query_plan.json`. 
Note: Ensure you have initialized a Go module in `/home/user` and fetched the official MongoDB Go driver (`go.mongodb.org/mongo-driver/mongo`).