You are a Database Administrator tasked with migrating and optimizing execution plans from a legacy document database to a new graph database. We need a cost estimator to evaluate NoSQL/Graph query execution plans. 

The costs for fundamental database operations were documented in an old system design chart, which is available as an image file located at `/app/plan_costs.png`. You will need to extract the mapping of operation names to their base costs from this image.

Your task is to write a Python script at `/home/user/plan_evaluator.py` that computes the total cost of a given query execution plan. 

The script must meet the following specifications:
1. It reads a single line of JSON from standard input (`sys.stdin`).
2. The JSON represents a nested query execution plan. Each node in the plan is a dictionary that contains at least an `"operation"` key (a string like `"INDEX_SCAN"` or `"HASH_JOIN"`).
3. A node may optionally contain child nodes under the keys `"left"`, `"right"`, or as a list of nodes under `"children"`.
4. The script must parse this cross-representational document and calculate the total query cost by summing the base cost of every operation present in the tree.
5. Use the operation costs extracted from `/app/plan_costs.png`. If an operation encountered in the JSON is NOT present in the image, its base cost should be evaluated as `0`.
6. The script should print ONLY the total integer cost to standard output (`sys.stdout`) and exit.

Example input format:
`{"operation": "HASH_JOIN", "left": {"operation": "INDEX_SCAN"}, "right": {"operation": "TABLE_SCAN"}}`

You may use standard tools like `tesseract-ocr` or write a quick script to extract the text from the image, but the final evaluator must be exactly robust and correct for any valid JSON plan matching the structure above.