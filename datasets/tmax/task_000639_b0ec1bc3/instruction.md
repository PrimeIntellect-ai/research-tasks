You are an e-commerce data engineer tasked with building an ETL pipeline to analyze purchase patterns and extract a specific graph-like relationship from relational data.

We have a set of relational CSV files in `/home/user/data/`:
1. `users.csv` (`user_id`, `name`)
2. `products.csv` (`product_id`, `category`)
3. `orders.csv` (`order_id`, `user_id`, `order_date`) - date format is `YYYY-MM-DD`
4. `order_items.csv` (`order_id`, `product_id`)

Your goal is to identify "influencer" users. 

Definition of an Influencer:
A user is an influencer if they purchase *any* product in a specific category on date $D$, and subsequently, at least 3 *other distinct* users purchase *any* product in that **same category** within the next 7 days (i.e., on dates between $D+1$ and $D+7$ inclusive). 

Instructions:
1. Write a Python script to process these CSV files. You may use standard libraries or install packages like `pandas` or `networkx`.
2. Cross-reference the relational tables to build a sequence of purchases per category.
3. Apply the pattern matching logic to find all `user_id`s that meet the influencer criteria. (If a user qualifies as an influencer multiple times or across different categories, they should only appear once in the final output).
4. Save the final list of influencer `user_id`s as a JSON formatted list of integers, sorted in ascending order, to the file `/home/user/influencers.json`.

Example of the output format in `/home/user/influencers.json`:
```json
[1, 5, 8]
```

Ensure your script runs successfully and produces the exact specified output file.