I am a researcher organizing a massive dataset of academic papers represented as an RDF Knowledge Graph. I need a C++ utility that can dynamically construct parameterized SPARQL 1.1 queries to filter, sort, paginate, and project this graph data. 

Please write a C++17 program at `/home/user/sparql_gen.cpp` and compile it to `/home/user/sparql_gen`. 

Your C++ program must accept the following command-line arguments:
- `--subject <uri>`: The URI of the research subject.
- `--min-year <int>`: The minimum publication year (inclusive).
- `--sort-by <string>`: The variable to sort by (either `year` or `citations`).
- `--limit <int>`: Pagination limit.
- `--offset <int>`: Pagination offset.

The program should output a strictly formatted SPARQL query to `stdout` based on these parameters. 

The query must strictly follow this template (replace the bracketed placeholders with the injected values from the CLI arguments, and omit the brackets):

```sparql
PREFIX ex: <http://example.org/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?paper ?title ?year ?citations
WHERE {
  ?paper ex:hasSubject <[SUBJECT_URI]> .
  ?paper foaf:title ?title .
  ?paper ex:year ?year .
  ?paper ex:citations ?citations .
  FILTER(?year >= [MIN_YEAR])
}
ORDER BY DESC(?[SORT_BY]) ASC(?paper)
LIMIT [LIMIT]
OFFSET [OFFSET]
```

Requirements:
1. Ensure the C++ program handles the arguments correctly. If an argument is missing, the program can behave undefined (assume valid input for testing).
2. The output must exactly match the formatting above, including indentation (2 spaces inside the WHERE block), capitalization, and line breaks.
3. Once the program is written and compiled (`g++ -std=c++17 -o sparql_gen sparql_gen.cpp`), create a bash script at `/home/user/generate.sh`.
4. The bash script must execute your C++ program exactly three times with the following parameter sets, appending the output of each run to `/home/user/queries.sparql` (separate each generated query with a single blank line):
   - Run 1: subject = `ex:MachineLearning`, min-year = `2018`, sort-by = `citations`, limit = `50`, offset = `0`
   - Run 2: subject = `ex:Bioinformatics`, min-year = `2020`, sort-by = `year`, limit = `10`, offset = `20`
   - Run 3: subject = `ex:QuantumComputing`, min-year = `2015`, sort-by = `citations`, limit = `100`, offset = `50`

Ensure the final `/home/user/queries.sparql` is correctly formatted. Make sure `/home/user/generate.sh` is executable and run it to produce the file.