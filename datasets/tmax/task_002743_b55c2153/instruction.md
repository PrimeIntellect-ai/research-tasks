You are helping a computational researcher organize a dataset of academic papers, authors, and citation networks. The dataset is provided as an RDF/Turtle file located at `/home/user/research_data.ttl`.

Your task is to write a Rust command-line application that processes this graph data using SPARQL, extracts specific metrics, and exports the results to a structured JSON format.

Dataset Schema Information:
- Prefixes: 
  `ex:` -> `<http://example.org/>`
  `dc:` -> `<http://purl.org/dc/elements/1.1/>`
  `foaf:` -> `<http://xmlns.com/foaf/0.1/>`
- Papers are entities with `a ex:Article`.
- Properties on Papers: 
  - `dc:title` (string literal)
  - `dc:date` (integer literal representing the year)
  - `ex:hasAuthor` (reference to an Author entity)
  - `ex:cites` (reference to another Paper entity that this paper cites)
- Properties on Authors:
  - `foaf:name` (string literal)

Task requirements:
1. Create a new Rust project at `/home/user/citation_query`. You may use the `oxigraph` crate (version `0.3.22` or similar) to parse the RDF file and execute SPARQL queries, and `serde_json` for exporting.
2. Write a SPARQL query and execute it in your Rust program to find the most cited articles published **after the year 2018** (i.e., `year > 2018`).
3. For each qualifying article, extract:
   - The article's title.
   - The publication year.
   - The number of times it has been cited by other articles in the dataset (incoming `ex:cites` edges).
   - A single string containing all author names of the article, separated by a comma and a space (e.g., "Alice Smith, Bob Jones"). The names in this string MUST be sorted alphabetically.
4. Filter out any articles that have 0 citations.
5. Sort the final results by the number of citations in descending order. If there is a tie, sort by the article's title in alphabetical (ascending) order.
6. Limit the output to the top 3 results (Pagination/Limiting).
7. The Rust program must export the results to exactly `/home/user/top_articles.json` as a JSON array of objects.

The output JSON file must strictly follow this structure:
```json
[
  {
    "title": "Example Paper Title",
    "year": 2019,
    "authors": "Author A, Author B",
    "citations": 5
  }
]
```

Build and run your Rust program so that `/home/user/top_articles.json` is generated correctly.