You are an AI assistant helping a researcher organize and query complex citation datasets. 

The researcher has built a custom C++ parsing library, `libdataset`, to handle their specific JSON dataset format. However, the library is currently failing to build. 

Your tasks are:
1. **Fix the Vendored Library**: 
   The source for `libdataset` is located at `/app/libdataset`. It currently fails to compile due to a configuration error in its build setup. Fix the perturbation so that running `make` successfully produces `libdataset.a`.

2. **Develop the Graph Projection Tool**:
   Write a C++ program at `/home/user/process.cpp`. This program must:
   - Include `/app/libdataset/dataset.h`.
   - Read the entire JSON dataset from standard input (`stdin`).
   - Parse the JSON using `std::vector<Paper> parse_dataset(const std::string& json_str);` provided by the library.
   - Take a single command-line argument: `min_year` (an integer).
   - Perform a graph projection: Filter the dataset to retain ONLY papers where `year >= min_year`. 
   - Materialize the citation relationships among the filtered papers. An edge exists from `A` to `B` if `A` cites `B`, and BOTH `A` and `B` are in the filtered set.
   - Print the resulting edges to standard output (`stdout`), one per line, in the format: `A -> B`.
   - The output must be strictly sorted: first by the source paper ID in ascending order, then by the target paper ID in ascending order. Do not print any extraneous text.

3. **Compile your Tool**:
   Compile your program to produce the executable `/home/user/process`. You will need to link against the fixed `/app/libdataset/libdataset.a`.

Example input JSON structure (handled by `parse_dataset`):
```json
{
  "papers": [
    {"id": 10, "year": 2020, "cites": [20, 30]},
    {"id": 20, "year": 2019, "cites": [30]},
    {"id": 30, "year": 2021, "cites": []}
  ]
}
```
If `./process 2020` is run, paper 20 is filtered out. The only remaining valid edge is `10 -> 30`.

Ensure your C++ code is robust and your output precisely matches the expected edge format.