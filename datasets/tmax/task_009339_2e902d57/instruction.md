I need a reproducible, multi-language data pipeline to process a CSV of mathematical concept descriptions, compute semantic embeddings, and retrieve the most relevant concept for a specific query.

Here is the setup:
You are provided with a file at `/home/user/math_concepts.csv`. It has two columns: `ID` and `Description`.

Please perform the following tasks:
1. **Embedding Generation (Python):** 
   Write a Python script at `/home/user/embed.py` that:
   - Reads `/home/user/math_concepts.csv`.
   - Uses the `sentence-transformers` library to load the `all-MiniLM-L6-v2` model.
   - Computes the embeddings for all the descriptions in the CSV.
   - Saves these embeddings to `/home/user/embeddings.csv` (no header, no index, each row represents the embedding of the corresponding CSV row).
   - Computes the embedding for the query string: `"A 2D shape with 4 equal sides and 90-degree angles."`
   - Saves this single query embedding to `/home/user/query.csv` (no header, no index, 1 row).

2. **Retrieval (R):**
   Write an R script at `/home/user/retrieve.R` that:
   - Reads `/home/user/embeddings.csv` and `/home/user/query.csv`.
   - Computes the cosine similarity between the query embedding and each of the concept embeddings.
   - Reads the original `/home/user/math_concepts.csv` to map the similarities back to their original `ID`s.
   - Writes the `ID` of the **single most similar** concept to a file named `/home/user/top_concept.txt`. The file should contain only this numeric ID.

3. **Reproducible Pipeline (Bash):**
   Write a bash script at `/home/user/run_pipeline.sh` that acts as the entry point. It must:
   - Install any necessary dependencies (e.g., `sentence-transformers`, `pandas` for Python; assume base R is installed but you may install R packages if strictly necessary, though base R is sufficient for matrix math).
   - Execute `embed.py`.
   - Execute `retrieve.R`.
   
Once you have written these scripts, give `/home/user/run_pipeline.sh` executable permissions and run it to produce `/home/user/top_concept.txt`. Do not use root privileges; install Python packages using `pip install --user` or in a virtual environment.