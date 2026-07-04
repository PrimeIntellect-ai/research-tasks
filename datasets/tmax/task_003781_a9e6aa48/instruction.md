You are assisting a researcher who is organizing large scientific collaboration datasets into a graph format. They store their dataset in a SQLite database. 

Currently, their data pipeline fails to map the relational tables into a graph correctly. Their SQL query generates an implicit cross join, resulting in massively inflated edge counts when calculating node degrees (co-author counts).

The exact schema, table names, column relationships, and filtering rules for the dataset are lost in text form, but the researcher has a screenshot of the documentation saved at `/app/schema_doc.png`. 

Your task:
1. Extract the schema, relationship mapping, and graph edge constraints from `/app/schema_doc.png` (Tesseract OCR is available on the system).
2. Write a Python script at `/home/user/graph_builder.py` that calculates the correct number of unique co-authors for a given researcher, according to the rules in the image.
3. The script must accept exactly two arguments:
   - `--db-path`: The path to the SQLite database file.
   - `--researcher-id`: The integer ID of the researcher whose co-author degree we are calculating.
4. The script must print *only* the integer count of unique valid co-authors to standard output (no extra text or logging on stdout).

Ensure your script performs the cross-representation mapping (relational to graph) efficiently and avoids the cross-join pitfalls the researcher encountered.