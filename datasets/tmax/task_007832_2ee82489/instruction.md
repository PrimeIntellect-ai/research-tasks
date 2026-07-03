You are a data engineer tasked with building a specialized Extract-Transform-Load (ETL) pipeline. Your goal is to process a raw NoSQL-style dump of event logs, project this data into a Knowledge Graph, and query it using SPARQL to uncover mutual engagement patterns.

You are provided with a raw data file located at `/home/user/events.ndjson`. This file contains JSON lines representing user events, with the following schema:
`{"user_id": "string", "event_type": "string", "target_user": "string"}`

Write a Python script (you may use standard libraries and `rdflib` which you'll need to install) to perform the following pipeline:

1. **NoSQL Aggregation Phase:** 
   Process the NDJSON file to compute the total number of "click" events for each `user_id`. Also, collect the set of all unique `target_user`s that each `user_id` has directed an event towards (of any `event_type`).

2. **Graph Materialization Phase:**
   Using the `rdflib` library, construct an in-memory RDF graph based on your aggregations. 
   - Define a namespace `ex = Namespace("http://example.org/")`.
   - Represent users as URIs like `http://example.org/u1`.
   - Add triples representing the total click counts: `<user_uri> ex:clickCount <count>`. The count must be an `rdflib.Literal` of datatype integer.
   - Add triples representing directed interactions: `<user_uri> ex:interactedWith <target_user_uri>`.

3. **SPARQL Query Phase:**
   Execute a SPARQL query against your constructed graph to find pairs of users (UserA and UserB) that meet ALL of the following conditions:
   - UserA `ex:interactedWith` UserB.
   - UserB `ex:interactedWith` UserA (mutual interaction).
   - UserA has an `ex:clickCount` >= 3.
   - UserB has an `ex:clickCount` >= 3.
   - UserA's ID is lexicographically less than UserB's ID (to avoid duplicate pairs in the output, e.g. "u1" < "u2").

4. **Result Export:**
   Export the results of your SPARQL query to a CSV file located at `/home/user/highly_active_mutuals.csv`.
   The CSV must have exactly this header: `userA,userB,clicksA,clicksB`
   The rows should contain the raw IDs (e.g., `u1`, not the full URI) and their respective click counts. Sort the CSV output by `userA` ascending, then `userB` ascending.

Make sure your script performs this entire pipeline and produces the output file at `/home/user/highly_active_mutuals.csv`. You may use `pip` to install necessary dependencies.