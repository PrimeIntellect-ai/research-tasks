You are an AI assistant helping a researcher organize and analyze a dataset of scientific papers. 

The researcher has a dataset of papers stored as a JSONLines file at `/home/user/papers.jsonl`. Each line is a JSON object representing a paper, with the following schema:
- `id` (string): Unique identifier for the paper.
- `authors` (list of strings): Authors of the paper.
- `references` (list of strings): IDs of other papers this paper cites.
- `topics` (list of strings): Topics associated with this paper.

Your task is to write a Python script `/home/user/analyze_graph.py` that processes this dataset to identify "influential" papers and discover the main topics of the research communities that build upon them. The script must execute the following logical pipeline without using external database systems (implement the logic in memory using Python's standard library):

1. **Knowledge Graph Pattern Matching**: Identify all "influential" papers. A paper is considered "influential" if it satisfies this exact graph pattern:
   - It is cited by **at least 3 distinct papers**.
   - **Each** of those citing papers must themselves be cited by **at least 1 other distinct paper**.

2. **NoSQL-style Aggregation Pipeline**: For each influential paper identified in step 1, analyze the papers that directly cite it. 
   - Extract all `topics` from these directly citing papers.
   - Count the frequency of each topic among the citing papers.
   - Determine the top 2 most frequent topics. If there is a tie in frequencies, resolve it by sorting the tied topic names alphabetically (A-Z) and picking the first ones.

3. **Output Generation**: The script must output a JSON file at `/home/user/influential_topics.json`. The output should be a JSON object where the keys are the `id`s of the influential papers, and the values are lists containing exactly the top 2 topics (as strings) determined in step 2.
Format example: `{"p1": ["AI", "Data"], "p99": ["Biology", "Genetics"]}`

Write the script and run it to produce the `influential_topics.json` file.