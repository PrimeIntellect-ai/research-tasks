You are an ML engineer preparing a preprocessing pipeline for a new training dataset. 

We have a configuration image located at `/app/config.png` that contains a single handwritten integer $k$, which represents our target truncation rank for a specialized matrix decomposition step.

Your task is to write a C program that performs a customized Truncated LU Decomposition. 
1. First, extract the integer $k$ from the image `/app/config.png` (you may use `tesseract` or any standard OCR tool).
2. Write a C program saved to `/home/user/truncate_lu.c` and compile it to `/home/user/truncate_lu`.
3. The program must read exactly 100 `double` (8-byte, little-endian) values from `stdin`, representing a 10x10 matrix $A$ in row-major order.
4. It must compute the standard LU decomposition of $A$ (assume no pivoting is required for the test data, $A=LU$).
5. It must then truncate both $L$ and $U$ to the first $k$ columns and $k$ rows respectively (where $k$ is the integer extracted from the image).
6. Multiply the truncated matrices back together: $A' = L_{10 \times k} \times U_{k \times 10}$.
7. Finally, output the resulting 10x10 matrix $A'$ to `stdout` as 100 `double` values in row-major order.

Ensure your program compiles without errors and strictly reads from `stdin` and writes to `stdout` without any extra text or formatting. Use standard libraries (or LAPACKE/cblas if installed and linked properly, though a simple custom Doolittle algorithm is sufficient for 10x10).