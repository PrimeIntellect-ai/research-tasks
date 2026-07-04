You are a script developer tasked with testing a new data serialization utility. 

We have a proprietary script at `/home/user/encode.py` that takes a list of integers and encodes them into a Base64 string. The encoding specification is as follows:
1. **Delta Encoding:** The first integer is kept as-is. Each subsequent integer is replaced by the difference between it and the previous integer (i.e., `delta[i] = nums[i] - nums[i-1]`).
2. **ZigZag Encoding:** Each delta is converted to a positive integer using ZigZag encoding: `z = 2 * v` if `v >= 0`, else `z = -2 * v - 1`.
3. **VLQ Encoding:** Each ZigZag integer is converted to a Variable-Length Quantity (VLQ) byte sequence. We use 7 bits per byte, big-endian order (most significant 7-bit groups first). The most significant bit (MSB) of each byte is set to `1` to indicate that more bytes follow, and `0` for the final byte of the integer.
4. **Base64:** The concatenated VLQ bytes for the entire sequence are encoded into a standard Base64 string.

Unfortunately, `/home/user/encode.py` is buggy and fails on certain inputs. Your task is to perform differential testing to isolate the failures:

1. **Generate Test Cases (Constraint Satisfaction):** Find all sequences of 5 integers $(x_1, x_2, x_3, x_4, x_5)$ that satisfy:
   - $-8 \le x_i \le 8$ for all $i$
   - $x_1 < x_2 < x_3 < x_4 < x_5$ (strictly increasing)
   - $\sum x_1+x_2+x_3+x_4+x_5 = 4$
2. **Implement Reference:** Write your own flawless reference implementation of the encoding specification.
3. **Execute and Diff:** Run both your reference implementation and `/home/user/encode.py` on all generated sequences. `/home/user/encode.py` can be imported as a module (`from encode import custom_encode`) or run as a script. 
4. **Report:** For every sequence where the output of `/home/user/encode.py` differs from your reference implementation, create a line formatted exactly like this:
   `[x1, x2, x3, x4, x5] | Expected: <reference_b64> | Actual: <buggy_b64>`
5. **Sort and Save:** Sort all the failure lines lexicographically (alphabetically) and save the final report to `/home/user/failures.txt`.

Ensure your reference implementation meticulously follows the VLQ big-endian, 7-bit payload specification.