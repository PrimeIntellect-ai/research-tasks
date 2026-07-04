You are an AI assistant acting as a technical compliance officer. We are auditing a company's internal systems for potential kickback schemes. 

A database dump from the company's internal tracking system has been provided to you at `/home/user/audit.db`. The database is a SQLite3 file, but the IT department did not provide any documentation about its schema. The database essentially acts as a property graph, storing various entities and their relationships over time.

Your task is to:
1. Reverse engineer the schema of `/home/user/audit.db`.
2. Construct a query or script to find a very specific "kickback" graph pattern.
3. The pattern we are looking for is defined by the following sequence of relationships:
   - A person (Employee A) `emails` another person (Employee B).
   - Later, Employee B `approves` a company (Vendor).
   - Later, the Vendor `pays` an account (Account).
   - Employee A `owns` that exact Account.
   
   *Note: The chronological order is strict: The email must happen before the approval, and the approval must happen before the payment. Ownership has no temporal constraints.*
4. Extract the names of the entities involved in this pattern.
5. Write the results to a CSV file located exactly at `/home/user/kickback_report.csv`.
   - The file must have the following exact header row: `employee_a,employee_b,vendor_name,account_name`
   - Include all instances of this pattern you find. If multiple exist, sort them alphabetically by `employee_a`, then `employee_b`.
   - Use the actual names of the entities as stored in the database, not their IDs.

You may use Bash, Python, or standard Linux tools to inspect the database and generate the report. Do not install massive external graph database software; use the provided SQLite file.