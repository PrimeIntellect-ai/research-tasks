You are a Database Administrator and C++ backend developer. We are migrating to a unified "Query Router" system that acts as a middleware between our frontend applications and our datastores (PostgreSQL for relational data, Redis for document/cache data). 

Currently, the system is broken and vulnerable to injection attacks. You must fix the multi-service orchestration, implement query sorting and pagination, and write an anti-injection sanitizer that passes our adversarial corpus tests.

**Part 1: Multi-Service Orchestration**
We rely on a stack consisting of Nginx, PostgreSQL, Redis, and our custom C++ Query Router.
1. Run `/app/start_services.sh` to initialize PostgreSQL (port 5432) and Redis (port 6379).
2. The Nginx configuration file is located at `/home/user/nginx.conf`. It is supposed to listen on port 8080 and proxy incoming JSON API requests to our C++ backend on port 8081, but the `proxy_pass` directive is missing or incorrect. Fix it and start Nginx using this config (`nginx -c /home/user/nginx.conf`).
3. The C++ Query Router source code is in `/home/user/query_router/`. Modify `config.hpp` so the service connects to PostgreSQL (db: `appdb`, user: `appuser`, password: `secret`, host: `127.0.0.1`, port: 5432) and Redis (host: `127.0.0.1`, port: 6379).

**Part 2: Result Processing & Pagination**
In `/home/user/query_router/db_handler.cpp`, the function `std::string execute_postgres_query(const std::string& base_query, int limit, int offset)` is incomplete. It currently ignores the `limit` and `offset` parameters, returning all rows. 
Modify this C++ function to append the correct SQL `LIMIT` and `OFFSET` clauses based on the integer arguments, and sort the results by the `id` column in ascending order to ensure consistent pagination mapping.

**Part 3: Adversarial Corpus Sanitizer**
Our security team has provided two directories of sample API requests:
* `/app/corpora/clean/`: Contains valid JSON request bodies that our system MUST process successfully.
* `/app/corpora/evil/`: Contains malicious JSON request bodies containing SQL injection payloads, NoSQL injections, and unauthorized system commands.

Your job is to implement the `bool is_safe_payload(const std::string& json_body)` function in `/home/user/query_router/sanitizer.cpp`. 
* Analyze the payloads in the clean and evil directories. 
* Write the logic to detect and block the malicious patterns found in the `evil` directory while allowing *everything* in the `clean` directory.
* If a payload is unsafe, the C++ HTTP server will return a `403 Forbidden` status. 
* Compile the C++ service using the provided `make` command in the `/home/user/query_router/` directory, and run the resulting `./query_router` binary in the background.

To successfully complete the task, all services must be running, connected, and your C++ service must correctly route through Nginx, returning paginated data for clean queries and blocking 100% of the evil payloads. Ensure the final binary is running and Nginx is successfully forwarding traffic on port 8080 before finishing.