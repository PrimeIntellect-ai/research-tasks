You are an AI assistant helping a data researcher organize and analyze a large collection of scholarly articles. The researcher models the datasets as a combined NoSQL/Graph structure, where documents have internal weights and citations form directed edges between them.

The researcher has left a photo of a whiteboard containing the custom "Relevance Score" formula they want to use, as well as the strict JSON schema required for the output pipeline. This image is located at `/app/relevance_formula.png`.

Your task is to write a Rust command-line tool that calculates this relevance score for a given dataset and outputs the results matching the whiteboard's schema.

Requirements:
1. **Analyze the Whiteboard Image:** Use OCR (e.g., `tesseract`, which is installed on the system) or write a quick vision script to extract the text from `/app/relevance_formula.png`. It contains the mathematical formula for the score and the required output JSON schema.
2. **Implement the CLI in Rust:** Write a Rust program that reads a JSON payload from standard input (`stdin`). 
   The input JSON will have the following schema:
   ```json
   {
     "nodes": [
       { "id": "A", "weight": 2.5 },
       { "id": "B", "weight": 1.2 }
     ],
     "edges": [
       { "src": "A", "dst": "B" }
     ]
   }
   ```
3. **Graph Analytics & Output:** For each node in the input, calculate the score according to the formula extracted from the image. 
4. **Validation & Formatting:** The program must print to standard output (`stdout`) a strictly formatted JSON array containing the results, matching the schema found in the image. The output array must be sorted alphabetically by the node ID. Do not print any extraneous text, logging, or formatting outside of the raw JSON.
5. **Compilation:** Compile your Rust program and place the final executable binary at exactly `/home/user/relevance_calc`. Ensure it is executable.

You have full freedom to initialize a Cargo project anywhere in `/home/user/` to develop your code, but the final binary must be copied or moved to `/home/user/relevance_calc`.