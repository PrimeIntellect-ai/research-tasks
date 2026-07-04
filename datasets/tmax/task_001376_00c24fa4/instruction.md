I am a researcher organizing hierarchical datasets. In our pipeline, we have an old, undocumented utility compiled as a binary located at `/app/sql_generator`. This tool is used to generate complex recursive SQL queries (Common Table Expressions) to trace dataset lineage (either upstream sources or downstream derived datasets). 

Unfortunately, we lost the source code for this utility. We are migrating our pipeline and need this tool rewritten in Python. 

Your task is to write a Python script at `/home/user/generate_query.py` that behaves EXACTLY like the `/app/sql_generator` binary. 

The binary accepts exactly three command-line arguments:
1. `DIRECTION`: Either `ANCESTOR` or `DESCENDANT`.
2. `TABLE_NAME`: The name of the database table (e.g., `datasets`).
3. `START_ID`: An integer representing the target dataset ID.

Example usage of the binary:
`/app/sql_generator ANCESTOR public_data 42`

Your Python script must accept these exact same three arguments and print out the EXACT same SQL string (character-for-character, including matching whitespace, indentation, and capitalization) as the binary. You should experiment with the binary in the terminal to figure out its exact output format and logic for both directions.

Write your complete solution to `/home/user/generate_query.py`.