I am a researcher organizing a NoSQL document dataset of academic publications, and I need your help extracting a specific citation graph metric.

I have a directory of JSON documents at `/home/user/dataset/`. Each JSON file represents a single publication and contains the following schema:
- `id`: (string) Unique identifier for the paper.
- `title`: (string) The title of the paper.
- `institution`: (string) The institution of the primary author.
- `citations`: (array of strings) A list of `id`s of other papers that this paper cites.

I need you to write a Bash script at `/home/user/analyze.sh` that performs the following data querying and aggregation pipeline:
1. **Cross-representation mapping**: Read all JSON documents in the dataset and map the data into a citation graph. Specifically, you need to reverse the edges: instead of looking at what a paper cites, you need to determine *which papers cite it*.
2. **Aggregation**: For every paper in the dataset, calculate the number of **distinct institutions** that cite it. (e.g., if Paper X is cited by 3 papers, but all 3 are from "University A", the distinct institution count for Paper X is 1).
3. **Sorting and Pagination**: Sort the results in descending order based on the count of distinct citing institutions. If there is a tie, sort alphabetically by the paper `id` in ascending order.
4. **Filtering/Output**: Output ONLY the top 3 results to a file named `/home/user/top_papers.json` in the following strict JSON array format:
```json
[
  {
    "id": "P_XYZ",
    "citing_institutions_count": 3
  },
  ...
]
```

Please execute your script to ensure `/home/user/top_papers.json` is generated correctly. I will be verifying the exact contents of `/home/user/top_papers.json`. You may use standard Linux utilities like `jq`, `awk`, `sort`, etc.