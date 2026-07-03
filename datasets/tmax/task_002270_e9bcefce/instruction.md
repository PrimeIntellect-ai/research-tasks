You are a data engineer tasked with building an ETL pipeline that extracts flat network data, loads it into a graph database, and queries it for a specific projection.

Your environment is a standard Linux terminal. You do not have `sudo` privileges, so any tools or services you need must be installed in your home directory (`/home/user`). Java 11+ is already installed on the system.

Here are the requirements for your task:

1. **Service Setup**:
   Download Apache Jena Fuseki version 4.8.0 from the official Apache archive (e.g., `https://archive.apache.org/dist/jena/binaries/apache-jena-fuseki-4.8.0.tar.gz`). 
   Extract it to `/home/user/fuseki` and start the Fuseki server in the background so it runs on the default port (3030). Configure it to run with an in-memory dataset named `/ds`.

2. **Data Ingestion (ETL via Go)**:
   A CSV file is located at `/home/user/network.csv`. It has the following headers: `subject,predicate,object`.
   Write a Go program at `/home/user/etl.go` that:
   - Reads the CSV file.
   - Maps the data into RDF triples. Assume a base URI of `http://example.org/` for all subjects, predicates, and objects.
   - Uses SPARQL UPDATE over HTTP (to `http://localhost:3030/ds/update`) to insert this data into the Fuseki server. You may need to batch the inserts or construct a valid `INSERT DATA` SPARQL query.

3. **Graph Query & Projection**:
   Extend your Go program (or write a new one at `/home/user/query.go`) to execute a SPARQL `SELECT` query against `http://localhost:3030/ds/query`.
   The query must find all distinct nodes that are reachable from the node `http://example.org/user1` via a **transitive** path consisting entirely of the `http://example.org/knows` predicate (i.e., people user1 knows, people they know, etc., of any depth >= 1).

4. **Output Schema Validation**:
   Your Go program must extract just the local names (e.g., `user2`, not the full URI) of the matching nodes. Sort these names alphabetically and write them to `/home/user/result.json` strictly matching this JSON schema:
   ```json
   {
     "source": "user1",
     "transitive_connections": [
       "user2",
       "user3"
     ]
   }
   ```

Ensure your Go code is properly formatted, handles HTTP errors gracefully, and outputs the exact JSON structure. 
Execute your pipeline to generate the final `/home/user/result.json` file.