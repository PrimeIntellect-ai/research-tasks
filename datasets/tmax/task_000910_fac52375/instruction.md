A junior data analyst has been trying to map our relational CSV data into a graph format. They wrote a Rust program to convert the CSV files into a Cypher script for Neo4j. Unfortunately, their relationship mapping logic had a flaw resembling an "implicit cross join" in SQL: it accidentally created a `KNOWS` relationship between *everyone* who lives in the same city, rather than using the actual `friendships.csv` table!

Your task is to fix this pipeline. 

In `/home/user/graph_builder`, you will find a basic Rust project. 
The raw data is located in `/home/user/data/`:
1. `cities.csv`: `id,name`
2. `users.csv`: `id,name,city_id`
3. `friendships.csv`: `user1_id,user2_id` (Note: Friendships are bidirectional. If 1 knows 2, 2 knows 1. The CSV only lists each pair once).

Write or update the Rust program in `/home/user/graph_builder` to perform the following:
1. Parse the CSV files accurately.
2. Generate a valid Cypher script at `/home/user/graph.cypher` that creates the graph without the cross-join bug. 
   To allow for automated testing, the Cypher file must have exactly this format and be sorted by IDs (ascending):
   - First, create all cities: `CREATE (:City {id: 1, name: 'CityName'});`
   - Second, create all users: `CREATE (:User {id: 1, name: 'UserName'});`
   - Third, create `LIVES_IN` relations (sorted by user id): `MATCH (u:User {id: 1}), (c:City {id: 1}) CREATE (u)-[:LIVES_IN]->(c);`
   - Fourth, create `KNOWS` relations (sorted by user1_id, then user2_id). Include BOTH directions since friendship is bidirectional: `MATCH (u1:User {id: 1}), (u2:User {id: 2}) CREATE (u1)-[:KNOWS]->(u2);`
3. Process the graph within the Rust code to answer this query: "What is the name of the user who is exactly a friend-of-a-friend (2 hops away in the KNOWS graph, excluding themselves and direct friends) of 'Alice' AND lives in 'Graphville'?"
   Write the name of this user to `/home/user/answer.txt`.

Make sure to run your Rust program so the `.cypher` and `.txt` files are generated.