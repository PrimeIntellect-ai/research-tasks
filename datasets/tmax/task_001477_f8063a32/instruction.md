You are assisting a researcher in organizing dataset relationships dictated in an audio recording. The researcher has recorded a series of statements describing how different database tables join together. 

Your task is to extract this graph of relationships and perform a graph-like query using SQLite and C.

Here are the steps to complete the task:
1. **Transcribe the audio:** An audio file is located at `/app/dataset_dictation.wav`. Use the `whisper` CLI tool (which is already installed in the environment) to transcribe this file to text.
2. **Parse the transcription with C:** Write a C program at `/home/user/parser.c` that reads the transcription text file. The transcription contains sentences resembling: "[TableA] joins with [TableB]". Your C program must parse these statements and extract the pairs into a CSV format (`source_table,target_table`). Compile and run it to produce `/home/user/edges.csv`.
3. **Database Operations:** Load `/home/user/edges.csv` into an SQLite database named `/home/user/schema.db` in a table called `edges`.
4. **Complex Query:** Write an SQLite query using a Common Table Expression (CTE) to find all tables that are exactly 2 hops away from the table `user_logs` (i.e., `user_logs` joins with table A, and table A joins with table B. You want to find all such 'table B's). 
5. **Output Export:** Execute the query, sort the resulting target table names alphabetically, and save them (one per line) to `/home/user/2hop_results.txt`.

Ensure your C code handles basic string matching and file I/O efficiently using standard libraries. Do not use external C libraries.