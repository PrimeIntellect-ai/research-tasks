We are processing a massive backlog of exported graph data in CSV format, representing a financial network. However, our upstream data ingestion pipeline has been heavily polluted with malformed subgraphs and adversarial transactions that violate our business logic data model.

As our lead data analyst, you need to write a standalone Go program that acts as a strict graph sanitizer. 

Here is what you need to know:
1. **The Schema Requirements:** The authoritative graph schema and traversal constraints have been physically diagrammed by our enterprise architects. I only have a scan of it located at `/app/schema.png`. You will need to extract the allowed node types, edge relations, and specific topological constraints (like forbidden cycles) from this image.
2. **The Data Format:** The CSV files you will process have no header and exactly 5 columns: `SourceID,SourceType,TargetID,TargetType,Relation`.
3. **The Deliverable:** Write a Go script at `/home/user/graph_validator.go`. It must accept exactly one argument: the absolute path to a CSV file. 
4. **The Output:** Your program must build an in-memory representation of the CSV's graph, check it against the rules from the image, and print strictly `ACCEPT` to standard output if the entire CSV is perfectly valid, or `REJECT` if any row or topological constraint is violated. Exit cleanly (exit code 0) in both cases.

We have a set of test files in `/app/corpora/clean/` (which your script should ACCEPT) and `/app/corpora/evil/` (which your script should REJECT). You can test your script against these before finalizing.

Ensure your code is highly optimized for graph traversal and uses appropriate data structures to detect cycles and validate reverse-engineered schema paths. `tesseract-ocr` is pre-installed on the system if you need to perform vision tasks in the terminal.