You are a database administrator tasked with creating a robust backend service that performs complex data querying and analytics on a dataset of financial transactions. 

You have been provided with two files:
1. `/app/transactions.jsonl`: A JSON Lines file containing transaction records. Each record has `src` (sender ID), `dst` (receiver ID), and `amount` (transfer amount).
2. `/app/architecture.png`: An image file containing the architectural specification and API schema for the service you need to build. You must extract the text from this image to understand the exact port, endpoints, and response formats required.

Your task is to write and run a web service (in Python, Node.js, or any other language) that satisfies the requirements outlined in `/app/architecture.png`. The service will need to:
- Construct a directed graph from the transactions to compute specific graph analytics metrics as requested in the image.
- Chain together data aggregations (simulating a NoSQL aggregation pipeline) to filter and summarize the transaction data based on dynamic parameters.
- Start an HTTP server listening on the exact host and port specified in the image, implementing the required endpoints.

Ensure that the service processes the `/app/transactions.jsonl` file correctly and starts the server in the background so it remains active. You may install any necessary packages (e.g., `flask`, `fastapi`, `networkx`, `tesseract-ocr`) to accomplish this.