You are a data analyst working for an internal corporate investigations team. You have been given two CSV dumps containing communication metadata, located in `/home/user/data/`.

1. `/home/user/data/employees.csv`
2. `/home/user/data/messages.csv`

You need to analyze the communication network to find the most influential employees. 

Your tasks are:
1. Examine the CSV files to understand their structure and how they relate to each other. 
2. Write a Python script that builds a directed graph of communications. The graph should use the message sender as the source node, the message receiver as the target node, and the sum of the message `bytes` between them as the edge weight.
3. Compute the PageRank for all employees in this directed, weighted graph. Use `networkx` in Python with the default parameters for PageRank (alpha=0.85), but ensure the `weight` parameter is set to use the aggregated bytes.
4. Join the graph results back to the employee data to get their actual names.
5. Export the top 3 employees with the highest PageRank scores to a JSON file at `/home/user/top_influencers.json`.

The output JSON file must be an array of objects, sorted in descending order by their PageRank score. Each object must have exactly these keys:
- `employee_id` (integer)
- `name` (string)
- `pagerank` (float)

Ensure your Python environment uses standard libraries plus `networkx` and `pandas`.