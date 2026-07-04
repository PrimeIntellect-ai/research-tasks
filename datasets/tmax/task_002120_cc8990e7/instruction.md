You are a database administrator tasked with analyzing and optimizing a social network graph stored in a SQLite database. 

A developer has dumped the current production schema and dataset into `/home/user/network.db`. The database contains a simple directed graph representation of user relationships, but it lacks proper indexing and the analytical queries are currently running too slowly.

Your task consists of two parts:

1. **Graph Querying & Analysis:**
   We need to calculate a specific marketing metric called "Extended Reach" for the user with the username `omega_node`.
   The "Extended Reach" is calculated as:
   `(Count of Unique Direct Followers * 1.0) + (Count of Unique Level-2 Followers * 0.5)`
   
   Definitions:
   - **Direct Follower:** A user who directly follows the target user.
   - **Level-2 Follower:** A user who follows ANY of the target user's Direct Followers. 
   - **Exclusions:** When counting Level-2 Followers, you MUST exclude anyone who is already a Direct Follower, and you MUST exclude the target user themselves.

   Write a query or script in your language of choice to calculate this metric for `omega_node`. Save the final numerical result (just the number, e.g., `42.5`) to `/home/user/reach.txt`.

2. **Schema Optimization:**
   The database currently has no indexes other than primary keys. Analyze the schema and relationships, then determine the optimal indexes that would speed up the calculation of the "Extended Reach" metric. 
   Create these indexes in `/home/user/network.db`. 
   Additionally, write the exact `CREATE INDEX` SQL statements you used into a file at `/home/user/indexes.sql`.

Ensure your calculations are highly accurate and your indexes appropriately target the foreign keys or lookup columns involved in the joins.