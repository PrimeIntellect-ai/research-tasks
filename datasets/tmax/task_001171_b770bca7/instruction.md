I am a researcher organizing large knowledge graph datasets. We have a legacy compiled C++ utility located at `/app/kg_matcher` that extracts specific 2-hop interaction patterns from our raw edge lists and exports them to a strictly validated JSON schema. Unfortunately, the original author left, the source code was lost, and the binary is stripped. We need to migrate this tool to Python to integrate it into our new data pipeline.

Your task is to write a Python script at `/home/user/kg_matcher.py` that is **behaviorally identical** to the `/app/kg_matcher` binary. 

Here is what I know about the tool:
1. It reads raw knowledge graph triples from `stdin`. The input consists of pipe-separated lines in the format: `subject|predicate|object`.
2. It takes exactly two command-line arguments representing a sequence of two predicates to search for. For example: `/app/kg_matcher "knows" "likes"`.
3. It performs a pattern match (a join) to find all 2-hop paths matching `(X) -[predicate1]-> (Y) -[predicate2]-> (Z)`.
4. It outputs the matched paths to `stdout` as a JSON array. 

You must reverse-engineer the exact matching logic, JSON keys, spacing, and sorting order by feeding test inputs to `/app/kg_matcher` and observing its output. 

Your final script must run via `python3 /home/user/kg_matcher.py <predicate1> <predicate2>` and produce **bit-exact** output compared to the original binary for any valid input. Please make sure your Python script is robust and handles standard input properly.