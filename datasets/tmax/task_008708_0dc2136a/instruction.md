I am a researcher organizing a messy dataset of academic papers. I need you to build a Python pipeline that validates the data, constructs a knowledge graph, and uses SPARQL to extract specific citation metrics. 

Here are the requirements:

1. **Setup:**
   You will find three files in my home directory (`/home/user/`):
   - `raw_papers.json`: An array of JSON objects representing papers, their authors, publication venues, and references (citations).
   - `input_schema.json`: A JSON Schema for a valid paper record.
   - `output_schema.json`: A JSON Schema for the final output.

   *Note: These files will be created by a setup script before you start. If they don't exist, please assume they will be there when the automated tests run, or create mock versions to write your code.*

2. **Validation (Schema):**
   Write a Python script that first reads `raw_papers.json` and filters out any records that DO NOT strictly conform to `input_schema.json`. Use the `jsonschema` library for validation. Ignore invalid records.

3. **Graph Construction (RDF):**
   Using the `rdflib` Python library, build an in-memory RDF graph from the *valid* papers. 
   Use the namespace `http://example.org/` (bind it to `ex:`).
   Model the data strictly as follows:
   - Paper entities: `ex:Paper_<id>`
   - Author entities: `ex:Author_<name>` (replace spaces with underscores)
   - Triples to create:
     - `ex:Paper_<id> ex:hasAuthor ex:Author_<name>`
     - `ex:Paper_<id> ex:publishedIn "<venue>"` (venue is a string literal)
     - `ex:Paper_<id> ex:cites ex:Paper_<cited_id>` (for each paper ID in the `cites` array)

4. **Graph Query (SPARQL):**
   Execute a SPARQL query on your constructed RDF graph to find the top 3 authors based on a specific metric: **The number of citations their papers have received specifically from papers published in the venue "Science".**
   - In other words, count how many times an author's papers are the *target* of an `ex:cites` relationship originating from a paper where `ex:publishedIn` is "Science".
   - Sort the results descending by the citation count. If there is a tie, sort alphabetically by the author's name.

5. **Output Generation & Validation:**
   Export the top 3 authors and their "Science citation counts" into a file named `/home/user/top_authors.json`.
   The output must be a JSON array of objects, e.g., `[{"author": "John_Doe", "science_citations": 5}, ...]`.
   Before saving, validate this output against `/home/user/output_schema.json` to ensure your pipeline produces correctly structured results.

You may install any necessary Python packages (like `rdflib` and `jsonschema`) using pip. Keep your processing script in `/home/user/process_graph.py` and execute it to generate the final `top_authors.json`.