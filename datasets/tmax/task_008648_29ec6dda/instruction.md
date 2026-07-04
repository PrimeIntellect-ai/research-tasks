You are a platform engineer troubleshooting a failing CI pipeline. We have a C-based backend utility that merges two sorted arrays of integers. In our CI environment, a property-based test suite is failing. 

Currently, the C application is designed to run as a simple TCP service (wrapped via `socat` in CI). Our architecture requires an Nginx reverse proxy to sit in front of this service to handle incoming connections.

Your task is to fix the bug, set up the proxy, and get the test suite to pass.

**Prerequisites & Setup Requirements:**
1. Install necessary dependencies: `nginx`, `socat`, `python3-pip`.
2. Install Python testing packages: `pytest`, `hypothesis` (you may need to use `--break-system-packages` if running pip in a modern Linux environment).

**System Components:**

1. **The C Backend (`/home/user/merger.c`)**:
   Create this file with the following buggy implementation. It reads two lines of space-separated integers from stdin, parses them, merges them into a single sorted output, and prints the result.
   ```c
   #include <stdio.h>
   #include <stdlib.h>
   #include <string.h>

   void parse_and_merge(char *line1, char *line2) {
       int arr1[1000], arr2[1000], out[2000];
       int n1 = 0, n2 = 0;
       
       char *token = strtok(line1, " \n");
       while (token != NULL) {
           arr1[n1++] = atoi(token);
           token = strtok(NULL, " \n");
       }
       
       token = strtok(line2, " \n");
       while (token != NULL) {
           arr2[n2++] = atoi(token);
           token = strtok(NULL, " \n");
       }
       
       int i = 0, j = 0, k = 0;
       while (i < n1 && j < n2) {
           if (arr1[i] < arr2[j]) {
               out[k++] = arr1[i++];
           } else if (arr1[i] > arr2[j]) {
               out[k++] = arr2[j++];
           } else {
               out[k++] = arr1[i++];
               j++; // Bug: Drops duplicate elements
           }
       }
       while (i < n1) out[k++] = arr1[i++];
       while (j < n2) out[k++] = arr2[j++];
       
       for (int x = 0; x < k; x++) {
           printf("%d%s", out[x], (x == k - 1) ? "" : " ");
       }
       printf("\n");
       fflush(stdout);
   }

   int main() {
       char line1[8192], line2[8192];
       if (!fgets(line1, sizeof(line1), stdin)) return 0;
       if (!fgets(line2, sizeof(line2), stdin)) return 0;
       parse_and_merge(line1, line2);
       return 0;
   }
   ```

2. **The Test Suite (`/home/user/test_merge.py`)**:
   Create this Python file to perform property-based testing on the service.
   ```python
   import socket
   from hypothesis import given, settings
   import hypothesis.strategies as st

   @settings(max_examples=100, deadline=1000)
   @given(st.lists(st.integers(min_value=-1000, max_value=1000), max_size=50),
          st.lists(st.integers(min_value=-1000, max_value=1000), max_size=50))
   def test_merge_service(list1, list2):
       list1.sort()
       list2.sort()
       
       expected = sorted(list1 + list2)
       
       # Connect to the Nginx reverse proxy
       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       s.connect(("127.0.0.1", 8080))
       
       msg = " ".join(map(str, list1)) + "\n" + " ".join(map(str, list2)) + "\n"
       s.sendall(msg.encode('utf-8'))
       
       data = s.recv(8192).decode('utf-8').strip()
       s.close()
       
       if not expected:
           assert data == ""
       else:
           actual = list(map(int, data.split()))
           assert actual == expected, f"Expected {expected}, got {actual}"
   ```

**Your Objectives:**
1. Fix the bug in `/home/user/merger.c` that causes the property-based tests to fail. The program must correctly preserve duplicate elements when merging.
2. Compile the fixed C program to `/home/user/merger`.
3. Create an Nginx configuration file at `/home/user/nginx.conf` that sets up a **TCP stream proxy** (not HTTP). It must listen on `127.0.0.1:8080` and proxy all connections to `127.0.0.1:9000`.
4. Start Nginx using your custom configuration.
5. Run the compiled `/home/user/merger` binary as a TCP service on port `9000` using `socat`. It should accept multiple connections concurrently and fork a new process for each connection.
6. Run the property-based tests using `pytest /home/user/test_merge.py`.
7. Save the output of the successful test run to `/home/user/test_results.log`.
8. Save a unified diff of your changes to `merger.c` in `/home/user/fix.patch` (comparing the original buggy version to your fixed version).