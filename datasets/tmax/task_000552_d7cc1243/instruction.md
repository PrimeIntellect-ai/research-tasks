You are tasked with building a robust C++ data ingestion pipeline that filters e-commerce transaction CSVs against multiple backend services. This pipeline must perform output schema validation, query reference data via complex joins, and sanitize adversarial inputs.

A startup script has already launched two services on your local environment:
1. PostgreSQL (Port 5432, DB: `commerce`, User: `analyst`, Password: `data`)
2. Redis (Port 6379, no password)

Your objective is twofold:

**Part 1: Backend Setup**
1. You have reference data at `/home/user/reference/users.csv` (schema: `user_id, name, account_status`) and `/home/user/reference/products.csv` (schema: `product_id, category, is_active`).
2. Create the corresponding tables in the PostgreSQL `commerce` database and load this reference data.
3. You have a Redis dataset script at `/home/user/reference/load_redis.sh` which populates a blacklist of fraudulent `txn_id`s. Execute it to populate Redis.

**Part 2: The C++ Sanitizer Pipeline**
Write a C++ program at `/home/user/workspace/sanitizer.cpp` and compile it to `/home/user/workspace/sanitizer`. You must use `libpq` for PostgreSQL and `hiredis` for Redis (both are installed in the environment).

The binary will be invoked via standard input/output:
`./sanitizer < input.csv > output.csv`

The input CSV has the schema: `txn_id,user_id,product_id,amount,notes`.
Your C++ program must read the CSV, validate and filter rows, and output ONLY the valid rows (including the original header). 

A row is VALID if and only if it passes ALL the following checks:
1. **No Blacklisted Transaction:** The `txn_id` MUST NOT exist as a key in the Redis database.
2. **Referential Integrity & Business Logic:** Using a single SQL query in your C++ code (involving a join), verify that the `user_id` exists in the `users` table AND the `product_id` exists in the `products` table. Furthermore, the user's `account_status` must be exactly `'VERIFIED'` and the product's `is_active` must be `true`.
3. **Adversarial Injection Filter:** The `notes` field MUST NOT contain any of the following SQL injection substrings: `DROP`, `--`, `;`, or `UNION` (case-sensitive).

Compile your code using standard flags (e.g., `g++ -O2 sanitizer.cpp -o sanitizer -lpq -lhiredis`). Make sure your program handles standard CSV parsing securely. An automated testing suite will evaluate your compiled `/home/user/workspace/sanitizer` binary against two hidden datasets.