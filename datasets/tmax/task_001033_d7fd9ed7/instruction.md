As an artifact manager curating binary repositories, we are migrating off an old, undocumented, proprietary tool used for normalizing artifact metadata paths. The legacy tool is provided as a stripped binary at `/app/legacy_indexer`.

We need to rewrite this tool in C++. We don't have the source code, but we know it reads messy artifact paths line-by-line from standard input and outputs a normalized, curated artifact tag to standard output. 

Your task is to:
1. Reverse-engineer or black-box test the behavior of `/app/legacy_indexer`. 
2. Write a C++ program at `/home/user/indexer.cpp` that implements exactly the same logic.
3. Compile your C++ program to an executable located at `/home/user/indexer`. 

Your executable must read from standard input, process the text identically to the legacy binary, and write to standard output. It must be bit-exact equivalent in its output for any given input sequence. Use standard C++ I/O (streaming).

Ensure the executable has execution permissions and is located exactly at `/home/user/indexer`.