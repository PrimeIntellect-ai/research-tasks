You are acting as a data engineer building an ETL pipeline to transform document-oriented data into a graph database format. 

We have an export of our NoSQL document store containing user purchase orders located at `/home/user/data/orders.json`. Your task is to write a C++ program that reads this document data, projects it into a graph model, and outputs a Cypher script that can be used to load the data into a Neo4j database efficiently.

Here are the requirements:

1. **Setup**: Create a directory `/home/user/etl`. Write your C++ source code in `/home/user/etl/generate_cypher.cpp`. You may use the `nlohmann/json` library for parsing JSON (you can download it via `wget https://github.com/nlohmann/json/releases/download/v3.11.2/json.hpp` to your working directory).

2. **Graph Projection Model**:
    * **Nodes**: 
        * `User` (with property `user_id` as string, and `name` as string)
        * `Product` (with property `product_id` as string, and `category` as string)
    * **Edges**:
        * `PURCHASED` (from `User` to `Product`, with property `price` as float and `quantity` as integer)

3. **Index Strategy Design**:
    * To ensure our `MERGE` statements are performant when the script is run on a real database, your output Cypher script MUST start with exactly these two index creation statements:
      `CREATE INDEX user_id_index FOR (u:User) ON (u.user_id);`
      `CREATE INDEX product_id_index FOR (p:Product) ON (p.product_id);`

4. **Cypher Generation**:
    * After the index statements, the C++ program must generate Cypher `MERGE` statements to idempotently create the nodes and relationships.
    * For each order in the JSON, generate:
      * A `MERGE` statement for the User.
      * A `MERGE` statement for the Product.
      * A `MERGE` statement for the `PURCHASED` relationship connecting them.
    * Example format for a single purchase:
      ```cypher
      MERGE (u:User {user_id: "U123"}) ON CREATE SET u.name = "Alice";
      MERGE (p:Product {product_id: "P456"}) ON CREATE SET p.category = "Electronics";
      MERGE (u)-[r:PURCHASED {price: 99.99, quantity: 1}]->(p);
      ```

5. **Execution**:
    * Compile your C++ program and run it.
    * The C++ program must output the final Cypher script to `/home/user/etl/import.cypher`.

You need to write the C++ program, compile it, run it against the `/home/user/data/orders.json` file, and ensure `/home/user/etl/import.cypher` is generated perfectly.