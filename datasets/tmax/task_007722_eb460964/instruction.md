You are a data engineer building an ETL pipeline to process a supply chain network. The network data is delivered as flat CSV files representing a graph of facilities (nodes) and transport routes (edges with distances).

Your goal is to process this raw data, calculate specific routes, paginate the results, and provide the equivalent graph database query for the downstream team.

The input data will be placed in two files:
1. `/home/user/nodes.csv` with columns: `id,name,type` (Types can be 'factory', 'warehouse', 'retail')
2. `/home/user/edges.csv` with columns: `source,target,distance` (distance is an integer)

**Part 1: Go Data Processing Pipeline**
Write a Go program at `/home/user/pipeline.go` that:
1. Parses the two CSV files.
2. Builds an in-memory graph. The graph is directed (edges go from `source` to `target`).
3. Computes the shortest path distance from the starting factory node (id: `N001`) to all nodes of type `warehouse`.
4. Filters the results to only include warehouses that are reachable with a total distance of `<= 150`.
5. Sorts the filtered results primarily by `distance` in **descending** order. If distances are equal, sort alphabetically by node `id` in **ascending** order.
6. Paginates the sorted results using a page size of `3` items per page.
7. Retrieves exactly **Page 2** (assuming 1-based indexing, i.e., items at index 3, 4, and 5 of the sorted list).
8. Writes this specific page of results as a JSON array to `/home/user/results.json`. Each object in the array should have the format: `{"id": "...", "name": "...", "distance": ...}`.

**Part 2: Cypher Query Design**
The downstream system uses Neo4j. Write the equivalent Cypher query that performs this exact same retrieval, filtering, sorting, and pagination. 
Save this query in a file at `/home/user/query.cypher`. 
Assume the nodes have labels `(:Facility {id: '...', name: '...', type: '...'})` and the relationships are `[:ROUTE {distance: ...}]`. 
Your query must:
- Match paths from the Facility with id `N001` to any Facility of type `warehouse`.
- Calculate the shortest path based on the relationship `distance` property (assume you are summing the distance properties along the path). *Note: You can use a standard variable-length path match or shortestPath, summing the distances.*
- Filter where total distance <= 150.
- Order by distance descending, then by id ascending.
- Return the `id`, `name`, and `distance`.
- Skip and limit to return Page 2 (items 4, 5, 6).

Compile and run your Go program to generate `/home/user/results.json`, and ensure `/home/user/query.cypher` is created.