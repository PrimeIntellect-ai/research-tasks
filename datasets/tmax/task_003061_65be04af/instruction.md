You are a Data Engineer building a strict data validation and sanitization gate for a complex ETL pipeline. Incoming hierarchical data batches frequently contain corrupted structures or violate strict compliance rules.

Your task is to build a CLI detector that reads a data batch, evaluates it against our compliance rules, and decides whether to accept or reject it.

However, the specific compliance rules were dictated in a voice memo by the Chief Compliance Officer, which is saved at `/app/compliance_memo.wav`. You will need to transcribe this audio file to understand the exact conditions for acceptance and rejection. 

**Data Format:**
Every data batch is provided as a directory containing two files:
1. `nodes.csv` - Contains columns: `id`, `department`, `timestamp`, `cost`
2. `edges.csv` - Contains columns: `parent_id`, `child_id` (representing the directed supply chain hierarchy)

**Your Objectives:**
1. Discover the business logic rules from `/app/compliance_memo.wav`.
2. Write an executable CLI tool at `/home/user/validate_batch`. 
3. The tool must accept a single argument (the path to a batch directory), load the data, execute the necessary SQL or programmatic checks (involving hierarchical processing and analytical windows), and output EXACTLY the word `ACCEPT` (if it passes all rules) or `REJECT` (if it violates any rule) to standard output.
4. Test your tool. We have provided two local sample corpora for your development:
   - `/app/corpus/clean/` : Contains several batch directories that strictly adhere to the rules and must be preserved (ACCEPTED).
   - `/app/corpus/evil/` : Contains several batch directories that contain malicious/corrupted data violating the rules and must be filtered out (REJECTED).

**Constraints:**
- You can use any programming language, database (SQLite is highly recommended for this data size), or libraries you prefer. You have full internet access to download tools like `ffmpeg`, `whisper`, or database drivers.
- Your final tool must be executable via `/home/user/validate_batch <path_to_directory>`.
- The evaluation will test your tool against a hidden set of clean and evil batches.