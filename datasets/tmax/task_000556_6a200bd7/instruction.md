You are a data analyst reviewing automatically generated product descriptions for an e-commerce platform. You have a raw CSV file containing the products and their generated descriptions, but the data is messy, and some of the AI-generated descriptions are either irrelevant or poorly formatted.

Your task is to write a Python pipeline that enforces data schema, validates the generated descriptions using embedding-based semantic similarity, and tests the outputs against specific constraints.

**Input Data:**
A CSV file located at `/home/user/products.csv` with the following columns:
`id`, `product_name`, `category`, `generated_description`

**Requirements:**
1. **Dependency Installation:** You will need to install any required Python packages (e.g., `pandas`, `sentence-transformers`, `scikit-learn`) in your user environment.
2. **Schema Enforcement:** Read the CSV file. Enforce a strict schema by completely dropping any rows that contain missing values (NaN, null, or empty strings) in ANY of the four columns.
3. **Embedding Computation:** Use the `sentence-transformers/all-MiniLM-L6-v2` model to compute embeddings for:
   - A combined reference string: `"{product_name} {category}"`
   - The generated string: `"{generated_description}"`
4. **Output Validation & Testing:** For each valid row, validate the description against two rules:
   - **Semantic Relevance:** The cosine similarity between the reference embedding and the generated description embedding must be strictly greater than `0.35`.
   - **Length Constraint:** The `generated_description` must contain between 5 and 30 words inclusive (words are determined by splitting the string by standard whitespace).
5. **Reporting:** If a row fails either or both constraints, it must be flagged.
   Create a JSON file at `/home/user/flagged_products.json` containing a list of dictionaries for the flagged products. Each dictionary must have exactly two keys:
   - `"id"`: The integer ID of the product.
   - `"failure_reason"`: A string indicating the failure. Must be exactly one of:
     - `"low_similarity"` (if it only fails the semantic relevance test)
     - `"invalid_length"` (if it only fails the length constraint)
     - `"both"` (if it fails both constraints)

Sort the final JSON array in ascending order by `"id"`.

Example expected format for `/home/user/flagged_products.json`:
```json
[
  {
    "id": 102,
    "failure_reason": "invalid_length"
  },
  {
    "id": 105,
    "failure_reason": "both"
  }
]
```