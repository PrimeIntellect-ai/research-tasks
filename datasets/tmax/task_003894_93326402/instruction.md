You are an expert data engineer. We have a multi-service infrastructure running locally that handles an organization's internal data. The setup includes a PostgreSQL database (relational data), a Neo4j database (graph data), and a Python FastAPI application serving as a Data API. 

Currently, our employee and department hierarchy data is trapped in a flat relational format in PostgreSQL, and the FastAPI application is incomplete and failing to start because it lacks the necessary environment configurations and query logic.

Your task is to build the ETL pipeline and configure the API service to expose this data:

1. **Service Configuration:**
   - Explore the `docker-compose.yml` or service configurations located in `/app/services/` to understand the running services (PostgreSQL, Neo4j, and the API base). 
   - Ensure the FastAPI application in `/app/api/main.py` is properly configured to connect to both databases. You will need to inject the correct environment variables or modify the configuration file `/app/api/.env`.

2. **ETL Pipeline Construction (Python):**
   - Write a Python script `/home/user/etl_pipeline.py` that connects to the PostgreSQL database.
   - Use a Recursive CTE (Complex SQL) to extract the full employee reporting hierarchy (who reports to whom, all the way up to the CEO) from the `employees` table.
   - Transform and load this hierarchical data into the Neo4j database. You must use parameterized Cypher queries to create `Employee` nodes and `REPORTS_TO` relationships.
   - Run the script to populate the graph database.

3. **API Implementation & Protocol Handling:**
   - Complete the `/app/api/main.py` FastAPI endpoints:
     - `GET /api/v1/hierarchy/{employee_id}`: Must execute a Cypher query against Neo4j to return the hierarchical path of managers for the given employee.
     - `GET /api/v1/cross-reference/{employee_id}`: Must query PostgreSQL for the employee's salary/department (using complex joins) and Neo4j for their direct reports, merging the result into a single JSON response.
   - The API must listen on `127.0.0.1:8080`.
   - The API must require a Bearer token for authentication. The valid token is `super-secret-etl-token`. Implement this in the FastAPI app so that unauthorized requests return a 401.

Ensure the API is running as a background process and listening on the required port when you are finished. Create a log file at `/home/user/api_startup.log` containing the startup logs of the FastAPI application to verify it is running.