We are migrating a legacy Python data pipeline into a high-performance C microservice. The legacy pipeline took two data sources, joined them by an `id` column, and calculated the Pearson correlation coefficient between the values. Because of how the legacy Python code worked, joining missing IDs introduced `NaN` values, silently converting integer columns to floats, and the correlation was calculated using *pairwise deletion* (ignoring rows where either value is missing).

We have lost the legacy Python source code, but we recovered a compiled, stripped Linux binary of the old logic at `/app/data_oracle`. This binary takes two CSV file paths as arguments and prints the expected correlation coefficient (formatted to 4 decimal places).

Your task:
1. Reverse-engineer or use `/app/data_oracle` as a black-box to understand its exact correlation calculation behavior (especially how it handles the "missing value" float conversions via joining).
2. Write a C program at `/home/user/server.c` and compile it to `/home/user/server`.
3. The C program must run a TCP server listening on `127.0.0.1:9000`.
4. When a client connects via TCP, it will send exactly two absolute paths to CSV files, separated by a newline (`\n`), and terminated by a null byte or EOF.
5. Your server must read the two CSV files (each containing `id,value` headers, followed by integer or float data), join them by `id`, calculate the Pearson correlation matching the exact behavior of `/app/data_oracle`, and send the resulting float back over the TCP connection formatted to 4 decimal places (e.g., `0.8452\n`), then close the client connection.
6. The server must continue listening for new connections after serving a client.

*Notes:*
- You must use C. You can use standard libraries (`stdio.h`, `stdlib.h`, `string.h`, `math.h`, `sys/socket.h`, etc.).
- Ensure your server is robust to missing IDs in either file (the core joining/validation logic).
- Start your server in the background before finishing the task.