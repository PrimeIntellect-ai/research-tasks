You are an AI assistant helping a researcher organize a large dataset of academic papers. The dataset is stored as a JSON Lines file (a common NoSQL export format) located at `/home/user/dataset.jsonl`. 

Each line in the file represents a paper and contains a JSON object with at least the following keys:
- `id` (string): A unique identifier for the paper.
- `field` (string): The research field (e.g., "cs", "neuroscience", "bio").
- `cited_by` (array of strings): A list of IDs of other papers that cite this paper.

Your task consists of two parts using Bash and standard CLI tools (like `jq`, `awk`, `grep`, `sort`, etc.):

**Part 1: Aggregation, Graph Analytics, and Pagination**
We need to analyze the degree centrality (i.e., the number of citations received, which is the length of the `cited_by` array) for papers specifically in the "neuroscience" field.
1. Filter the dataset to only include papers where `"field"` is `"neuroscience"`.
2. Calculate the degree centrality for each of these papers.
3. Sort the papers primarily by their degree centrality in descending order. If there is a tie, sort them secondarily by their `id` in ascending (alphabetical) order.
4. Apply pagination to the sorted results. Assuming each "page" contains exactly 3 items, extract the items for **Page 2** (i.e., the 4th, 5th, and 6th items in the sorted list).
5. Output the `id`s of these 3 papers, one per line, to a file named `/home/user/page2_results.txt`.

**Part 2: Index Strategy Design**
To speed up future lookups for "neuroscience" papers without scanning the entire file or parsing JSON every time, you need to create a simple line-number index.
1. Find the exact line number (1-indexed) in the original `/home/user/dataset.jsonl` file for every "neuroscience" paper.
2. Format each entry as `id:line_number`.
3. Sort this index alphabetically by `id` in ascending order.
4. Save the formatted and sorted index to `/home/user/neuro_index.txt`.

Ensure your output files exactly match the specified formats.