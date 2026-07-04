You are a data analyst tasked with extracting underlying themes from a set of customer support tickets using natural language processing and linear algebra. 

There is a dataset located at `/home/user/tickets.csv` with two columns: `ticket_id` and `text`.

Your objective is to process this text, construct a document-term matrix, apply dimensionality reduction, and save the projected coordinates. 

Please perform the following steps:
1. Set up your Python environment and install any necessary libraries (e.g., `pandas`, `scikit-learn`, `numpy`).
2. Read `/home/user/tickets.csv`.
3. Tokenize the `text` column with the following strict rules:
   - Convert all text to lowercase.
   - Replace any character that is not a lowercase letter (`a-z`) or whitespace with a single space.
   - Split the text into tokens using standard whitespace separation.
4. Build a Document-Term Count Matrix where each cell represents the frequency of a word in a document. 
   - Only include words that appear in **at least 2 different documents** (document frequency >= 2).
   - The vocabulary columns must be sorted alphabetically.
5. Apply Principal Component Analysis (PCA) to reduce the count matrix down to 2 components. 
   - Use scikit-learn's `PCA`.
   - Set `n_components=2`, `random_state=42`, and `svd_solver='full'`.
6. Output a CSV file to `/home/user/topics.csv` containing the document projections.
   - The columns must be exactly: `ticket_id`, `pc1`, `pc2`.
   - Round the `pc1` and `pc2` values to exactly 4 decimal places.
   - Ensure the output is sorted by `ticket_id` in ascending order.