You are a web developer working on a backend feature that processes geospatial analytics from a frontend web canvas. Users submit polygon coordinates, and the backend needs to compute the areas of these polygons. To protect the service, you also need to implement basic request validation and rate limiting.

You have been given a log of incoming requests in `/home/user/requests.txt`. Each line represents a request and is formatted as follows:
`[Timestamp] [UserID] [x1,y1 x2,y2 x3,y3 ...]`
- `Timestamp`: An integer representing milliseconds. The file is sorted chronologically.
- `UserID`: An integer between 1 and 100.
- `x,y`: Pairs of floating-point numbers representing the vertices of a polygon in order.

Your task is to write a C program `/home/user/process_requests.c` that does the following:
1. Parses the `/home/user/requests.txt` file. You should define custom C structs to hold the request data and polygon vertices.
2. Implements a rate limiter: A user is only allowed a maximum of 2 requests within any rolling 1000 ms window. If a request arrives and the user already has 2 or more accepted requests strictly within the last 1000 ms (i.e., `current_timestamp - previous_timestamp < 1000`), the new request must be REJECTED and ignored.
3. Implements a numerical algorithm to calculate the area of the polygon for ACCEPTED requests. Use the Shoelace formula. The area should be absolute (positive).
4. Writes the results of the accepted requests to `/home/user/results.csv`.

The output file `/home/user/results.csv` must contain one line for each ACCEPTED request in the exact format:
`UserID,Area`
Where `Area` is formatted to exactly one decimal place (e.g., `45.5`).

Compile your program to `/home/user/process_requests` using `gcc` and run it to produce the output file.