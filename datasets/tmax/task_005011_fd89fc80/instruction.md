You are helping a computational researcher organize and query an academic dataset. The researcher has an SQLite database at `/home/user/research.db` containing local publication records, but needs to merge this local co-authorship network with external data from Wikidata.

Your task is to write a script (in any language) at `/home/user/get_network.py` (or similar, depending on your language choice, but assuming you run it) that takes an `author_id` (integer) as a command-line argument and performs the following:

1. **Complex Graph Traversal (Local):** Query the SQLite database to find all authors within a co-authorship distance of 2 from the target `author_id`. 
   - Distance 1 = direct co-authors (shared at least one paper).
   - Distance 2 = co-authors of direct co-authors.
   - The target author should NOT be in the results. An author at distance 1 should NOT also appear at distance 2.
   
   The database schema is:
   - `authors` (`id` INTEGER PRIMARY KEY, `name` TEXT, `wikidata_q` TEXT)
   - `papers` (`id` INTEGER PRIMARY KEY, `title` TEXT)
   - `author_paper` (`author_id` INTEGER, `paper_id` INTEGER)

2. **Schema Validation:** Export the local network findings to a JSON file named `/home/user/network_<author_id>.json`. The JSON *must* strictly match this structure:
   ```json
   {
     "target_author": <int>,
     "network": [
       {
         "author_id": <int>,
         "name": <string>,
         "distance": <int>,
         "wikidata_q": <string>
       }
     ]
   }
   ```
   (Sort the `network` array by `distance` ascending, then `author_id` ascending).

3. **Parameterized SPARQL Construction:** To fetch external data, the script must generate a valid SPARQL query file named `/home/user/wikidata_<author_id>.rq`. 
   - The query must use a `VALUES` clause to inject the Wikidata IDs (`wikidata_q`) of all authors found in step 1 (e.g., `VALUES ?author { wd:Q222 wd:Q333 }`).
   - The query should select `?author`, `?dob`, and `?employer` where `?dob` is the date of birth (`wdt:P569`) and `?employer` is the employer (`wdt:P108`).

**Action required:**
Write the script, then execute it for `author_id` 1:
`python3 /home/user/get_network.py 1` (or equivalent for your language).

Ensure the two output files (`/home/user/network_1.json` and `/home/user/wikidata_1.rq`) are correctly generated.