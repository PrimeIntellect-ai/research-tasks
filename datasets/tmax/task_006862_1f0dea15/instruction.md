You are an AI assistant helping a data researcher organize and analyze a complex dataset of academic papers, authors, and citation networks.

The researcher has data stored across multiple formats:
1. **Relational Data**: A SQLite database at `/home/user/data/authors.db` containing an `authors` table:
   - `author_id` (TEXT)
   - `name` (TEXT)
   - `institution` (TEXT)
2. **Document Data**: A JSON lines file at `/home/user/data/papers.jsonl` where each line is a JSON object representing a paper:
   - `paper_id` (String)
   - `title` (String)
   - `authors` (Array of Strings - author_ids)
   - `citations` (Array of Strings - paper_ids that this paper cites)

Your task is to write a Go program (`/home/user/workspace/analyze.go`) that performs cross-representation mapping, graph analytics, and pattern matching on this data, and outputs the result into a strictly validated JSON file.

### Objectives
1. **Initialize the Go Module**: Create a Go module in `/home/user/workspace` (e.g., `go mod init graphviz`). You may use standard libraries and community packages (like `github.com/mattn/go-sqlite3` for SQLite).
2. **Load Data**: Read and map the data from both the SQLite database and the JSONL file.
3. **Graph Analytics (Centrality)**: 
   - Compute the **In-Degree Centrality** (total number of incoming citations) for every paper.
   - Identify the `paper_id` with the highest in-degree centrality. If there is a tie, pick the one that comes first alphabetically.
4. **Knowledge Graph Pattern Matching**:
   - Find all **"Author Self-Citation Triads"**. 
   - A self-citation triad is defined as a sequence of three distinct papers (A, B, C) where:
     - Paper A cites Paper B
     - Paper B cites Paper C
     - Paper C cites Paper A
     - There is at least one `author_id` that is present in the `authors` array of **all three papers** (A, B, and C).
5. **Output Schema**:
   Your Go program must output the results to `/home/user/workspace/results.json` strictly matching this JSON schema:
   ```json
   {
     "highest_centrality_paper": "paper_id",
     "triad_patterns": [
       {
         "shared_author_id": "author_id",
         "papers": ["paper_id_1", "paper_id_2", "paper_id_3"]
       }
     ]
   }
   ```
   *Note*: The `papers` array inside `triad_patterns` should be sorted alphabetically to ensure determinism. Each unique triad-author combination should only appear once.

Build and run your Go program so that `/home/user/workspace/results.json` is generated correctly.