You are a data engineer tasked with building a robust, concurrent ETL pipeline in Go. We have international customer review data and a product catalog that need to be processed, joined, and aggregated.

Your goal is to write a Go program at `/home/user/pipeline.go` that performs the following tasks:

1. **Extraction and Unicode Processing (Node A)**: 
   Read the file `/home/user/data/reviews.txt`. Each line contains a customer review in various languages (English, Spanish, Japanese, etc.). You must extract:
   - The Product ID, which is always enclosed in square brackets (e.g., `[PRD-123]`).
   - The star rating, which is represented by the number of Unicode star characters (`⭐`, U+2B50) present in the line.

2. **Catalog Processing (Node B)**:
   Read the file `/home/user/data/products.csv`. This file contains the columns `ProductID,Category,Price`. 

3. **Join and Aggregate (Node C)**:
   Join the extracted reviews with the product catalog using the `ProductID`. Calculate the average star rating for each `Category`. 

**Pipeline DAG Requirements:**
Your Go program must implement a basic concurrent DAG (Directed Acyclic Graph) execution model. Specifically, Node A (Review Extraction) and Node B (Catalog Processing) must run concurrently using Go goroutines. The main routine (or a separate Node C goroutine) must wait for both A and B to complete using channels or `sync.WaitGroup` before performing the join and aggregation.

**Output:**
The program should create a JSON Lines (JSONL) file at `/home/user/output.jsonl`. 
Each line should be a JSON object containing the category and its average rating (rounded to two decimal places, or as a precise float if exactly representable), formatted exactly as:
`{"category":"Electronics","average_rating":4.0}`
Ensure the file is sorted alphabetically by category name.

To complete the task, execute your Go program so that `/home/user/output.jsonl` is generated. 

(Note: You can assume the data directory and input files already exist on the system).