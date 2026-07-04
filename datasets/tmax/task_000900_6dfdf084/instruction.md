I am a researcher organizing a massive publications dataset. I need your help to quickly expose a graph-like querying endpoint over my document database so my team can extract co-authorship networks.

Here is what you have to work with:
1. A dataset of publications in JSON Lines format located at `/home/user/data/papers.jsonl`. Each line is a document representing a published paper, containing a `paper_id` and an array of `authors` (author IDs).
2. A scanned image of my whiteboard at `/app/whiteboard.png`. I scribbled the specific Primary Author ID we are currently investigating on this whiteboard. You will need to extract this ID (tesseract is installed on the system).

Your task:
1. Extract the Primary Author ID from the whiteboard image. 
2. Create an aggregation pipeline (using `jq`, Python, or standard bash tools) that acts like a graph traversal: find all unique authors who have co-authored at least one paper with the Primary Author (excluding the Primary Author themselves).
3. Expose this pipeline via a simple HTTP web service listening on `0.0.0.0:8080`.
4. The service must have an endpoint `GET /api/graph/coauthors`.
5. When `GET /api/graph/coauthors` is called, your server should execute the pipeline and return the result as a JSON array of string author IDs (e.g., `["A-102", "A-304"]`).
6. Leave the server running in the background or foreground so my automated testing tools can issue requests to it.

Ensure your JSON response is properly formatted and contains ONLY the unique co-authors.