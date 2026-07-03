You are assisting a researcher who is organizing a large dataset of maritime trade routes. The dataset was recently corrupted due to a buggy SQL query containing an implicit cross join, which resulted in "phantom routes"—routes that traverse edges that do not actually exist in the physical trade network. 

We need to build a filter to separate the valid routes from the corrupted ones.

Here is what you need to do:
1. **Extract the true graph topology:** The canonical physical trade network is stored in an image at `/app/hub_graph.png`. Use OCR (e.g., `tesseract`, which is preinstalled) to extract the text from this image. The image contains a list of valid, directed edges, one per line in the format `SourceNode->DestNode` (e.g., `A->B`).

2. **Write a Go route validator:** Create a Go program at `/home/user/filter.go` and compile it to `/home/user/filter`. 
   - The program must accept a single file path as a command-line argument.
   - The input file will contain multiple routes, one per line. A route is represented as a comma-separated list of nodes showing the traversal path (e.g., `A,B,C,D`).
   - For every route in the file, your program must check if every step in the traversal exists as a valid directed edge in the true graph topology you extracted.
   - If *all* routes in the provided file are 100% valid, the program must exit with status code `0`.
   - If *any* route in the file contains an invalid transition (a phantom route), the program must exit with status code `1`.

Make sure your Go program is efficient, as it will be used to process large dumps of aggregated query results. You can hardcode the valid edges into your Go program after you extract them from the image, or have the program read the extracted text file—either approach is fine.