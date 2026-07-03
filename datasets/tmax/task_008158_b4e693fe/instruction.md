You are acting as a data researcher organizing and synthesizing datasets for a meta-analysis. I have two datasets located in `/home/user/data/`:

1. `/home/user/data/publications.ttl`: An RDF graph dataset (Turtle format) containing academic publications, their authors, and their research topics.
2. `/home/user/data/experiments.jsonl`: A document-based dataset (JSON Lines format) acting as a dump from a NoSQL database, containing experimental results and metrics associated with publication IDs.

Your task is to write a Python script at `/home/user/aggregate_research.py` that performs the following steps:
1. Load the RDF graph and execute a **SPARQL query** to extract all publications that have the topic `http://example.org/topic/MachineLearning`, along with the names of their authors.
2. Load the JSON Lines NoSQL data and use a data-processing pipeline (you can use Python's built-in tools or `pandas`) to aggregate the experimental metrics (`accuracy` and `f1_score`) per publication. Calculate the average of these metrics for each publication.
3. Perform **cross-query aggregation**: Join the authors from the SPARQL query with the aggregated experimental metrics. Calculate the overall average `accuracy` and `f1_score` for each author across all their Machine Learning publications.
4. **Export and format conversion**: Save the final aggregated results to a CSV file at `/home/user/author_metrics.csv`.

The output CSV must meet these strict formatting rules:
- Columns exactly named and ordered: `Author,Avg_Accuracy,Avg_F1`
- The `Author` column should contain the raw string name (e.g., "Alice Smith").
- The numeric columns (`Avg_Accuracy` and `Avg_F1`) must be rounded to exactly 4 decimal places.
- The rows must be sorted alphabetically by the `Author` column.

You may install any required Python packages (e.g., `rdflib`, `pandas`) using `pip`. Run your script to generate the final `/home/user/author_metrics.csv` file.