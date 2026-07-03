You are acting as a data analyst and tools developer. We are processing large dependency graphs exported as CSV files. 

Our senior analyst left a voice memo at `/app/analyst_notes.wav` with the exact traversal and filtering rules for our new dependency querying tool. 

Your task is to:
1. Transcribe the audio file `/app/analyst_notes.wav` to understand the exact knowledge graph pattern matching and recursive hierarchical query rules required.
2. Write a C++ program at `/home/user/kg_query.cpp` that implements this querying logic.
3. The program must take exactly two command-line arguments:
   - `argv[1]`: The absolute path to a CSV file. The CSV has no header and contains three columns: `source,target,relationship_type`.
   - `argv[2]`: The starting `source` node ID (a string).
4. The program must parse the CSV, perform the recursive query defined in the audio memo starting from the given node, and print the results to standard output.
5. Compile your program to `/home/user/kg_query` using standard C++17 (e.g., `g++ -std=c++17 -O2 /home/user/kg_query.cpp -o /home/user/kg_query`).

The system will verify your compiled program by running it against hundreds of randomly generated CSV files and comparing its output bit-for-bit against a reference implementation. Ensure your output format matches the requirements from the audio exactly.