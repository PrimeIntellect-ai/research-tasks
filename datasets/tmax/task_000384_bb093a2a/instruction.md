A researcher is organizing a complex dataset of historical academic interactions represented as an RDF graph. They need a robust utility to compute shortest connection paths between entities, but they have a specific filtering rule that was written on a whiteboard and captured in a photo.

Your task is to write a Python script `/home/user/query_distance.py` that calculates the shortest path length between two nodes in the provided RDF dataset, respecting the constraint shown in the image.

Here are the details:
1. **Dataset**: A graph in Turtle format is located at `/home/user/dataset.ttl`.
2. **Image Constraint**: There is an image at `/app/filter_rule.png` showing a whiteboard note. It specifies a certain RDF predicate URI that must be **completely ignored/excluded** during the path traversal (e.g., negative interactions or retracted citations).
3. **Script Interface**: You must write a Python 3 script that takes exactly two positional arguments: the source URI and the target URI.
   Usage: `python3 /home/user/query_distance.py <source_URI> <target_URI>`
4. **Implementation details**: 
   - You may use the `rdflib` library (you can install it via pip if needed) and SPARQL queries or `networkx` to compute the path.
   - The graph is unweighted (each edge has a weight of 1).
   - Edges are directed. You must traverse them in the forward direction.
5. **Output Schema**: The script must print exactly one integer to standard output representing the shortest path length (number of edges). If the target is not reachable from the source, output `-1`. Do not print any other text, warnings, or debug information.

Ensure your script is perfectly deterministic and highly robust, as it will be heavily tested with random pairs of URIs from the dataset.