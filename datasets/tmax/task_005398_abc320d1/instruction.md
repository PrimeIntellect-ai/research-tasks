You are acting as a Database Administrator and C++ Developer. You have been given a poorly documented SQLite database at `/home/user/ecommerce.db`. 

Your objective is to reverse engineer the schema, optimize it, write an analytical query, and build a C++ reporting tool to process the results.

Perform the following steps:

1. **Reverse Engineer the Schema:** 
   Analyze the database `/home/user/ecommerce.db`. It contains tables related to categories, products, orders, and order items. Identify the schema and relationships.

2. **Write an Analytical Query:**
   Write a SQL query and save it in `/home/user/query.sql`. The query must find the top 2 revenue-generating products for each category, but ONLY considering orders placed in the year '2023'. 
   - Revenue is calculated as `SUM(order_items.quantity * products.price)`.
   - Use window functions (specifically `DENSE_RANK()`) to assign a rank (1 for highest revenue, 2 for second highest). 
   - Order the final result by `category_name` ASC, `rank` ASC, `product_name` ASC.
   - The selected columns should be: `category_name`, `product_name`, `total_revenue`, `rank`.

3. **Optimize the Database:**
   Write a SQL script at `/home/user/optimize.sql` that creates at least two indexes to optimize the execution plan of your query (e.g., targeting date filtering and join columns). Execute this script against the database.

4. **Result Processing in C++:**
   Write a C++ program at `/home/user/report_generator.cpp` that:
   - Connects to `/home/user/ecommerce.db` using the SQLite3 C/C++ API.
   - Reads and executes the SQL query from `/home/user/query.sql`.
   - Processes the result set and writes it to a CSV file at `/home/user/top_products.csv`.
   - The CSV should have a header: `category_name,product_name,revenue,rank`.
   - The `revenue` should be formatted to exactly 2 decimal places.
   
   Compile your program using:
   `g++ -O3 -o /home/user/report_generator /home/user/report_generator.cpp -lsqlite3`
   
   Then run `/home/user/report_generator`.

Ensure your C++ program safely handles database connections and correctly parses the specific data types returned by your analytical query.