You are tasked with optimizing a highly inefficient data extraction microservice for a retail company. The service is written in Rust and interacts with a MongoDB backend. Currently, when multiple analytical jobs run concurrently, the system grinds to a halt due to terrible query plans and resource exhaustion, effectively deadlocking the database layer.

The source code for the microservice is located in `/home/user/analytics_service`.

Your objectives are:
1. **Start the Services:** Run the initialization script `/home/user/start_services.sh`. This script will launch a local MongoDB instance on port 27017, seed it with 200,000 order documents in the `retail.orders` collection, and start a mock load-generator.
2. **Analyze and Optimize the Query:** The Rust microservice contains a NoSQL aggregation pipeline in `/home/user/analytics_service/src/queries.rs`. It retrieves the total amount spent per category for a specific customer. Currently, it does a full collection scan, unwinds all items, and filters at the very end. 
   - Refactor the Rust code to optimize this aggregation pipeline (e.g., filter early).
   - Fix the query construction: it currently uses unsafe string concatenation. Convert it to use proper parameterized BSON document construction (e.g., using the `doc!` macro) to prevent parsing overhead and potential injection.
3. **Database Operations:** Create any necessary indexes in the MongoDB database (`retail` database, `orders` collection) to support your optimized query. You can do this via the `mongosh` CLI or by adding initialization code in the Rust app.
4. **Export Format:** Ensure the Rust microservice's `/export` endpoint correctly writes the query results to `/home/user/results.ndjson`. Each line must be a valid JSON object with the format: `{"category": "Electronics", "total_spent": 1250.50}`.
5. **Run the Service:** Compile and start the Rust service on port 8080 (`cargo run --release`).

The success of your task will be measured by an automated load test that hits the `http://localhost:8080/export?customer_id=CUST_999` endpoint 500 times concurrently. Your optimizations must ensure the 95th percentile latency is significantly reduced.