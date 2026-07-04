You are a data engineer building a custom ETL pipeline tool in C. You need to extract relational data from an SQLite database, map it into a nested document (JSON) structure, and export the queried results.

Your task is to write a C program that performs a specific paginated query and data transformation.

1. **Database Location**: An SQLite database exists at `/home/user/ecommerce.db`.
   It contains three tables:
   - `customers` (`id` INTEGER PRIMARY KEY, `name` TEXT, `region` TEXT)
   - `orders` (`id` INTEGER PRIMARY KEY, `customer_id` INTEGER, `total` REAL)
   - `order_items` (`id` INTEGER PRIMARY KEY, `order_id` INTEGER, `product_name` TEXT)

2. **Query & Filtering Requirements**:
   - Filter to only include customers from the region `'Europe'`.
   - Sort the filtered customers by their `id` in **ascending** order.
   - Paginate the customers: We want **Page 2** where the **page size is 2** (i.e., skip the first 2 customers, and take the next 2).
   - For these specific 2 customers, retrieve all their `orders`.
   - For each order, retrieve all the `product_name`s from `order_items`.

3. **Cross-Representation Mapping & Export**:
   - Map the relational data into a nested JSON document array.
   - The JSON should have the exact following schema for the output:
     ```json
     [
       {
         "customer_id": 123,
         "name": "John Doe",
         "orders": [
           {
             "order_id": 456,
             "total": 99.50,
             "items": ["Laptop", "Mouse"]
           }
         ]
       }
     ]
     ```
   - Export this JSON to exactly `/home/user/output.json`. Formatting (whitespace/indentation) does not matter as long as it is valid JSON and structurally identical to the schema.

4. **Implementation Constraints**:
   - You must write the solution in C (`/home/user/etl.c`).
   - You may download the SQLite amalgamation (`sqlite3.c` and `sqlite3.h`) or any single-file JSON C library (like `cJSON`) directly into `/home/user/` to compile alongside your program, as you do not have root access to install system packages.
   - Compile your program into an executable `/home/user/etl_bin` and run it so that `/home/user/output.json` is generated.