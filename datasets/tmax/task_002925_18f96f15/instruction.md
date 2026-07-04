You are assisting a data researcher in organizing a large collection of scientific dataset metadata. The metadata is stored as an RDF graph in Turtle format. The researcher uses a proprietary legacy tool to generate cryptographic checksum digests of dataset collections, but now needs to expose this capability via a modern web API for their automated pipeline.

Your task is to build a Python-based HTTP web service that queries the RDF knowledge graph, formats the results, uses the legacy binary to compute a digest, and returns the data.

Here are the exact requirements:

1. **The Knowledge Graph**: 
   Assume there is a Turtle file located at `/home/user/datasets.ttl` containing metadata about datasets, their authors, and their subject domains. (You do not need to create this file; it already exists).

2. **The Legacy Binary**:
   There is a stripped, packed legacy executable located at `/app/dataset_hasher`. It takes a list of dataset URIs (one URI per line) via standard input (`stdin`) and prints a single alphanumeric hash string to standard output (`stdout`).

3. **The Web Service API**:
   You must write and run a Python HTTP service (using standard libraries, Flask, or FastAPI; `rdflib` and `flask` are installed in the environment) that listens on `127.0.0.1:9090`.
   
   It must expose a single endpoint:
   `GET /api/search`
   
   It must accept two query parameters:
   - `author`: The URI of the author (e.g., `http://example.org/researcher/alice`)
   - `domain`: The URI of the research domain (e.g., `http://example.org/domain/biology`)
   
   It must require an authentication header:
   `Authorization: Bearer GraphOrgSecret`
   If the header is missing or incorrect, return a `401 Unauthorized` status code.

4. **Query and Processing Logic**:
   When the `/api/search` endpoint is called, your service must:
   - Construct a parameterized SPARQL query to find all dataset URIs (let's say variable `?dataset`) where the dataset has an `http://purl.org/dc/terms/creator` matching the `author` parameter, AND an `http://purl.org/dc/terms/subject` matching the `domain` parameter. (Assume the dataset URIs are the subjects of these triples).
   - Execute the SPARQL query against `/home/user/datasets.ttl` using Python's `rdflib`.
   - Extract the matching dataset URIs and sort them alphabetically.
   - Pass the sorted URIs (separated by a newline `\n`) to the standard input of the `/app/dataset_hasher` binary.
   - Capture the resulting hash string from the binary's output.

5. **Response Format**:
   The service must return a `200 OK` HTTP status with a JSON payload in this exact format:
   ```json
   {
     "results": [
       "http://example.org/dataset/1",
       "http://example.org/dataset/2"
     ],
     "digest": "abc123hashstring"
   }
   ```

Start the web service in the background or leave it running in the terminal so it can accept requests. Do not hardcode the expected outputs; your service must perform the SPARQL query and binary invocation dynamically per request.