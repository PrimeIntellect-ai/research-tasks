You are a developer tasked with organizing a messy directory and writing a small utility to verify our REST-to-gRPC route mappings using a custom checksum algorithm. 

First, organize the project space:
1. Create the directories: `/home/user/project/src`, `/home/user/project/data`, and `/home/user/project/build`.
2. Move `/home/user/project/routes.txt` into `/home/user/project/data/`.

Second, write a C program at `/home/user/project/src/mapper.c` that parses the `routes.txt` file and computes a mathematical checksum for each mapped endpoint. 
The `routes.txt` file contains lines mapping a REST URL route to a gRPC method name, formatted as:
`<URL_ROUTE> -> <GRPC_METHOD>`

Your C program must perform the following:
1. Read the input file line by line.
2. For each line, parse the URL route and the gRPC method.
3. Remove any URL parameters enclosed in curly braces `{}` from the URL route (e.g., `/api/v1/users/{id}` becomes `/api/v1/users/`). Remove the braces and the text inside them.
4. Calculate `Sum_URL`: the sum of the exact ASCII values of all characters in the stripped URL string.
5. Calculate `Sum_Method`: the sum of the exact ASCII values of all characters in the gRPC method string.
6. Calculate the checksum using this formula: `(Sum_URL * Sum_Method) % SEED_VAL`, where `SEED_VAL` is an integer defined via a compile-time macro `SEED`.
7. Output the results to a file specified as the second command-line argument (the first being the input file). The output should contain one line per route exactly matching this format:
`Checksum: <VALUE> | Method: <GRPC_METHOD>`

Third, use conditional compilation to build two separate executables in the `/home/user/project/build/` directory:
- Compile `mapper.c` into `/home/user/project/build/mapper_prod` with the macro `SEED` set to `17`.
- Compile `mapper.c` into `/home/user/project/build/mapper_test` with the macro `SEED` set to `31`.

Finally, execute both binaries using `/home/user/project/data/routes.txt` as the input. 
- Have `mapper_prod` output its results to `/home/user/project/build/output_prod.log`.
- Have `mapper_test` output its results to `/home/user/project/build/output_test.log`.