You are a data scientist tasked with cleaning 3D trajectory datasets. You need to build a C++ data sanitiser that processes time-series data, filters out anomalous points using rolling aggregations and distance metrics, and acts as a quality gate.

We have a vendored C++ library located at `/app/lib-ts-window-0.5` that provides efficient rolling window computations. However, it seems to be failing to compile in our environment due to a configuration issue. 

Your tasks are:
1. Fix the compilation issue in the vendored package `/app/lib-ts-window-0.5`. You are allowed to modify its `Makefile` or source files to get it to compile successfully as a static library (`libtswindow.a`).
2. Write a C++ program at `/home/user/cleaner.cpp` and compile it to `/home/user/cleaner`. Link it with the `libtswindow.a` library.
3. Your program must read a CSV file from standard input. The CSV has the header `timestamp,x,y,z` (where x, y, z are floats).
4. Implement a validation checkpoint: The program must verify that the `timestamp` values are strictly increasing. If a row has a timestamp less than or equal to the previous row, drop that row.
5. Implement a rolling window aggregation: For each valid row, maintain a sliding window of the up to the last 5 valid points (including the current point).
6. Compute the centroid (mean of `x`, `y`, and `z`) of the current window.
7. Compute the Euclidean distance between the current point and the window's centroid.
8. If this distance is greater than `10.0`, the point is considered an anomaly. Drop the point (do not include it in future windows).
9. Print the accepted rows to standard output in the exact same CSV format (including the header).

Your solution will be tested against two sets of CSV files:
- A "clean" corpus, where your program must preserve and output 100% of the rows.
- An "evil" corpus containing noisy, anomalous points, which your program must successfully detect and reject. 

Ensure your program handles standard input properly and compiles without errors. The compilation command you use should look something like `g++ -std=c++17 -I/app/lib-ts-window-0.5/include /home/user/cleaner.cpp -L/app/lib-ts-window-0.5/lib -ltswindow -o /home/user/cleaner`.