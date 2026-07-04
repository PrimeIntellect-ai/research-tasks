You are a data analyst investigating a routing network where some of the routing tables were corrupted. 

Most of the intact network edges are provided in a CSV file located at `/home/user/network.csv`. Each line has the format `source,target,weight` (all integers).
However, a crucial patch of updated edges was only provided as a screenshot of a spreadsheet, located at `/app/patch.png`. 

Your task is to:
1. Extract the missing edge data from the image `/app/patch.png`. The image contains text in the same `source,target,weight` format. You can use preinstalled tools like `tesseract` to extract this text.
2. Write a C program that reads the edges from `/home/user/network.csv` and merges them with the updated edges from the image. If an edge (same source and target) exists in both, use the updated weight from the image.
3. Build a directed graph representation in your C program.
4. Compute the shortest path from node `0` to all other reachable nodes in the network.
5. Calculate the average shortest path distance from node `0` to all reachable nodes (excluding node `0` itself, and excluding unreachable nodes).
6. Write this single floating-point number to `/home/user/metric_result.txt` (formatted to at least 4 decimal places).

Make sure your C program compiles cleanly and runs efficiently.