You are a data analyst acting as a query engineer. We have a set of custom CSV files containing scientific publication data. Standard database engines are unavailable on this system, so you must write a high-performance C++ tool to answer a specific parameterized graph-query over these CSVs.

The dataset consists of three CSV files located in `/home/user/data/`:
1. `authors.csv`: `author_id,name`
2. `papers.csv`: `paper_id,title,domain,citation_count`
3. `authors_papers.csv`: `author_id,paper_id`

You must write a C++17 program at `/home/user/query_engine.cpp` that processes these files. The program must accept three command-line arguments:
`./query_engine --domain <domain_name> --top <N> --out <output_file_path>`

The program must perform the equivalent of the following query/analysis:
1. Filter all papers that belong to the specified `<domain_name>`.
2. Find all authors who have written at least one paper in that domain.
3. For each of these authors, calculate their `domain_citations` (the sum of `citation_count` for all papers they authored *within the specified domain*).
4. Calculate each author's `coauthor_degree` within the domain. This is the number of *unique* other authors with whom they share at least one paper in the specified domain.
5. Rank the authors based on `domain_citations` in descending order. If there is a tie, sort by `author_id` in ascending order.
6. Take the top `<N>` authors from this sorted list.
7. Output the result to the specified `<output_file_path>` as a strictly formatted JSON array of objects.

Output JSON Schema requirement (do not include extra whitespace, format exactly like this on a single line):
`[{"author_id":<id>,"name":"<name>","domain_citations":<count>,"coauthor_degree":<count>},...]`

Rules & Constraints:
- Use only standard C++17 libraries. No external libraries (e.g., no Boost, no nlohmann/json). You must write your own lightweight CSV parsing and JSON string formatting.
- The CSV files have headers.
- Assume well-formed CSVs without embedded commas in the names/titles for this specific dataset.
- Compile your program to `/home/user/query_engine` using `g++ -O3 -std=c++17`.
- Once compiled, run your tool with the arguments: `--domain AI --top 2 --out /home/user/result.json`.

Ensure the final JSON file at `/home/user/result.json` is perfectly formatted and contains the correct query results.