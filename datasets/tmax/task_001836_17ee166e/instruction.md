You are a data engineer building an ETL pipeline that translates an internal custom querying DSL into optimized Cypher queries for a downstream graph database.

We have a legacy system that generates custom graph query requests. You need to write a fast, standalone C program that reads these requests from standard input (line by line) and outputs the corresponding, optimized Cypher queries to standard output.

First, inspect the image located at `/app/schema_rules.png`. This image contains a table mapping our internal domain entities to the actual Graph Node Labels, Edge Types, and Properties used in our Neo4j database. You will need to use OCR (e.g., using `tesseract`) to extract these exact schema rules.

Write a C program at `/home/user/cypher_generator.c` and compile it to an executable named `/home/user/cypher_generator`.

Your C program must parse standard input for the following custom DSL commands and output the exact corresponding Cypher string on a single line:

1. `MATCH_HIERARCHY <EntityName> <StartID> <MaxDepth>`
   Must output a Cypher query that finds the hierarchical tree using the recursive edge defined in the image for the given entity, starting from the node with `id = <StartID>`, up to `<MaxDepth>` hops.
   *Format*: `MATCH (n:<MappedNode> {id: "<StartID>"})-[r:<MappedRecursiveEdge>*1..<MaxDepth>]->(m:<MappedNode>) RETURN n, r, m;`

2. `AGGREGATE_REACH <EntityName> <StartID>`
   Must output a Cypher query that computes the count of all distinct nodes reachable via the recursive edge.
   *Format*: `MATCH (n:<MappedNode> {id: "<StartID>"})-[:<MappedRecursiveEdge>*]->(m:<MappedNode>) RETURN count(DISTINCT m) as total_reach;`

3. `FIND_INTERSECT <EntityName1> <ID1> <EntityName2> <ID2>`
   Must output an optimized Cypher query (using a CTE/WITH clause) that finds common adjacent nodes between the two entities. 
   *Format*: `MATCH (a:<MappedNode1> {id: "<ID1>"})-->(common)<--(b:<MappedNode2> {id: "<ID2>"}) RETURN common;`

Ensure your generated Cypher strings use the exact Node Labels and Edge Types recovered from the image. For example, if the input is `MATCH_HIERARCHY Employee E123 3`, and the image maps `Employee` to `Worker` and its recursive edge to `MANAGES`, you output:
`MATCH (n:Worker {id: "E123"})-[r:MANAGES*1..3]->(m:Worker) RETURN n, r, m;`

Compile your program with `gcc -O3 /home/user/cypher_generator.c -o /home/user/cypher_generator`. The automated verifier will pipe thousands of randomized DSL commands into your binary and verify that the output perfectly matches the reference query engine.