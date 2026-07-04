You are an AI assistant helping a researcher organize and aggregate their datasets. 

The researcher has two raw data files in `/home/user/`:
1. `categories.csv`: A comma-separated file representing a taxonomy of academic subjects. The columns are `id,parent_id,name`. If `parent_id` is empty, the category is a root category. Some categories are deeply nested (e.g., child of a child).
2. `papers.jsonl`: A JSON-lines file containing metadata about research papers. Each line represents a paper and contains fields like `"id"`, `"category_id"`, and `"citations"`.

Your task is to write a C program `/home/user/aggregate.c` that performs a cross-dataset hierarchical aggregation. 

The C program must do the following:
1. Parse `categories.csv` and internally build a hierarchy (simulating a recursive query) to map every `id` to the `name` of its ultimate **root** category.
2. Parse `papers.jsonl` (simulating a NoSQL aggregation pipeline). Extract the `category_id` and `citations` for each paper. (You may assume the JSON is strictly formatted on a single line so standard C string functions like `strstr` or `sscanf` are sufficient without a full JSON library).
3. Aggregate the total number of citations for each root category.
4. Write the results to a file named `/home/user/report.txt`. 

The format of `/home/user/report.txt` must be exactly:
```
[Root Category Name]: [Total Citations]
```
The lines must be sorted alphabetically by the Root Category Name. 

Compile your C program using `gcc /home/user/aggregate.c -o /home/user/aggregate` and run it to produce the `report.txt` file.