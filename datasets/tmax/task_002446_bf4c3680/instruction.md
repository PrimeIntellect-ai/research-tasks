You are helping a researcher organize and cross-reference a hybrid dataset consisting of a relational database and a semantic knowledge graph. 

The researcher has provided two datasets in the `/home/user/datasets/` directory:
1. `topics.ttl`: An RDF dataset (in Turtle format) containing a taxonomy of research topics. Relationships are defined using the `rdfs:subClassOf` property.
2. `authors.db`: An SQLite database containing metadata about authors and their publications. It contains two tables:
   - `authors` (`author_id` INTEGER PRIMARY KEY, `name` TEXT)
   - `papers` (`paper_id` INTEGER PRIMARY KEY, `title` TEXT, `author_id` INTEGER, `topic_uri` TEXT)

Your task is to write a Python script at `/home/user/process_data.py` that accomplishes the following:
1. Use a SPARQL query (via the `rdflib` library, which you may need to install) to find the target topic `<http://example.org/topics/ArtificialIntelligence>` and ALL of its subtopics, recursively, using the `rdfs:subClassOf` property. Ensure you capture the target topic itself as well as any direct or indirect subtopics.
2. Connect to the SQLite database and retrieve all papers that belong to any of the discovered topic URIs. You must perform a SQL join to associate these papers with their authors.
3. Export the combined results to a JSON file located at `/home/user/ai_authors.json`. 

The output JSON must strictly follow this format:
- A single JSON object where the keys are Author Names (string).
- The values are arrays of Paper Titles (strings) that the author wrote within the AI topics.
- The array of paper titles for each author must be sorted alphabetically.
- Only include authors who have at least one paper in the matched topics.
- The JSON file should be nicely formatted (indent=2).

Example output format:
```json
{
  "Dr. Alice Smith": [
    "A Survey of Deep Learning",
    "Understanding Neural Networks"
  ],
  "Dr. Bob Jones": [
    "NLP Techniques"
  ]
}
```

Run your script to generate the `/home/user/ai_authors.json` file.