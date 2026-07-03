You are acting as an AI assistant for a Compliance Officer who is auditing an organization's IT systems. 

The security team has exported an undocumented data model of the organization's identity and access management (IAM) system into an N-Triples-like CSV format, along with a week's worth of access logs.

You need to write a Go program that reverse-engineers this data model, performs graph analytics to determine user privileges, and cross-references these privileges against actual access logs to find compliance violations.

**Data Provided (Assume these exist before you start):**
1. `/home/user/data/graph.csv` - Contains the IAM graph. It has no header, and uses a `subject,predicate,object` format.
2. `/home/user/data/logs.csv` - Contains system access logs. It has a header: `timestamp,user_id,system_id`.

**Requirements for your Go program (`/home/user/audit.go`):**
1. **Data Model Reverse Engineering & Graph Traversal**:
   - Parse `graph.csv` to build an in-memory graph.
   - The graph contains entities like Users, Roles, and Systems. The predicates linking them are undocumented, but you can deduce them by observing the data. 
   - *Rule*: A User is authorized to access a System *only if* there is a path in the graph from the User to a Role, and from that Role to the System.
2. **Graph Analytics (Degree Centrality)**:
   - Calculate the "Authorized Access Centrality" for every User. This is defined as the total number of *unique* Systems a User is authorized to access based on the graph.
3. **Cross-Query Aggregation (Compliance Check)**:
   - Parse `logs.csv`.
   - Identify all "Unauthorized Access" events. An unauthorized access occurs when a user accesses a system they are not authorized for.
   - Aggregate these violations by user and system, counting the number of unauthorized attempts.
4. **Output Generation**:
   - The program must write its results to `/home/user/compliance_report.json`.
   - The JSON format must strictly match the following structure:
     ```json
     {
       "centrality": {
         "U1": 3,
         "U2": 1
       },
       "unauthorized_accesses": [
         {
           "user_id": "U2",
           "system_id": "SYS_DB",
           "count": 1
         }
       ]
     }
     ```
   - *Note*: The `unauthorized_accesses` array should only include user/system pairs with a count > 0, and should be sorted alphabetically by `user_id`, then by `system_id`.

**Action Items**:
1. Inspect the provided CSV files to understand the specific predicates used in `graph.csv`.
2. Write the Go program at `/home/user/audit.go`.
3. Initialize the Go module (`go mod init audit` in `/home/user/`).
4. Run your Go program to generate `/home/user/compliance_report.json`.