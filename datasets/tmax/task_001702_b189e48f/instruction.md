You are an AI assistant helping a data researcher organize and analyze a dataset of sparse vectors representing document embeddings. 

The researcher has an ETL process that has dumped large amounts of chunked data into `/home/user/data/chunks/`. Each CSV file in this directory contains sparse vector data for different items, formatted as:
`item_id,feature_index,feature_value`

There is also a query vector located at `/home/user/data/query.csv`, formatted as:
`feature_index,feature_value`

Your task is to compute the dot product between the query vector and every item in the dataset. Since the files can technically be very large, you should use standard Unix text-processing tools (like `awk`, `sort`, etc.) or a small, efficient script in a language of your choice to process the data out-of-core.

Find the `item_id` that has the highest dot product score with the query vector. 

Create a file at `/home/user/best_match.txt` containing exactly one line with the `item_id` and its dot product score, separated by a comma (e.g., `item_123,4.56`). 

Ensure your computation precisely handles negative numbers and standard float formatting.