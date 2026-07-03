You are helping me clean and process a dataset of event logs. 

First, there is an image containing configuration parameters located at `/app/config.png`. Please extract the text from this image (you can use `tesseract`). It will contain two lines:
1. `WINDOW=<number>` (the rolling window size for our aggregation)
2. `IGNORE=<token>` (a token that should be completely filtered out from our dataset)

Next, process the large dataset located at `/home/user/dataset.csv`. The file is encoded in ISO-8859-1. Each line contains three comma-separated fields: `timestamp` (integer), `token` (string), and `value` (float). 

Your task is to write a multi-stage pipeline using C as the primary language to:
1. Read the dataset and properly handle the character encoding, converting the strings to UTF-8.
2. Tokenize and normalize the data by dropping any rows where the token exactly matches the `IGNORE` token extracted from the image.
3. Group the records by `token` and sort them by `timestamp` in ascending order.
4. For each token's time-series, calculate the rolling simple moving average of the `value` field using the window size `WINDOW` extracted from the image. If there are fewer than `WINDOW` elements so far for a token, the average should be calculated over the available elements.
5. Find the maximum moving average achieved for each token.

Finally, write and start a TCP server in C listening on `127.0.0.1:9090`. 
The server must accept incoming TCP connections. When a client sends a token string followed by a newline (`\n`), the server should respond with the maximum moving average for that token, formatted to two decimal places, followed by a newline. If the token is not found or was ignored, respond with `NOT_FOUND\n`. The server should handle multiple sequential requests and remain running.

Ensure your server is compiled, running, and listening on port 9090 before you finish.