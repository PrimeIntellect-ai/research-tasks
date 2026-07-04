You are a data engineer tasked with building a multilingual ETL pipeline to process product catalog data. 

You need to write a Python script `/home/user/pipeline.py` that processes a messy JSON catalog and a CSV inventory file, then outputs a clean Parquet file.

**Input Files (already exist on the system):**
1. `/home/user/inputs/catalog.json`: Contains product descriptions in multiple languages (English, Spanish, Japanese). It has duplicates and messy Unicode representations (e.g., full-width characters, unnormalized accents, ideographic spaces).
2. `/home/user/inputs/inventory.csv`: Contains `id`, `price`, and `stock`.

**Pipeline Requirements:**
Your script must implement a DAG-like orchestration where the following steps are executed in order. You must log the completion of each step to `/home/user/outputs/pipeline.log` by writing `Step <step_name> completed\n`.

**Step 1: Extract & Deduplicate (Log: `Step extract completed`)**
- Read both files.
- Deduplicate the JSON data based on the `id` field, keeping only the **first** occurrence of each `id`.

**Step 2: Clean & Normalize (Log: `Step clean completed`)**
- Normalize the `desc` field in the JSON data using Unicode **NFKC** normalization.
- Strip leading and trailing whitespace from the `desc` field.
- Replace any consecutive whitespace characters inside the `desc` field with a single standard space (` `).

**Step 3: Feature Extraction (Log: `Step extract_features completed`)**
- Create a new column/field called `category`.
- If the normalized `desc` contains any of the following substrings (case-insensitive): `"shoe"`, `"zapato"`, `"靴"`, set `category` to `"Footwear"`.
- If it contains `"shirt"`, `"camiseta"`, `"シャツ"`, set `category` to `"Apparel"`.
- Otherwise, set `category` to `"Other"`.

**Step 4: Join & Load (Log: `Step load completed`)**
- Perform an inner join between the cleaned JSON data and the CSV inventory data on the `id` field.
- The final dataset must have the columns: `id`, `desc`, `category`, `price`, `stock`.
- Write the final dataset to `/home/user/outputs/final_catalog.parquet`.

**Constraints:**
- You may use standard libraries, `pandas`, and `pyarrow` (you will need to install any required packages via `pip`).
- Make sure to create the `/home/user/outputs/` directory before writing to it.