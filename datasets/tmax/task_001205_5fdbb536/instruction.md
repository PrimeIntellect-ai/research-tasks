Hello IT Support,

We have an open ticket (#9921) regarding a legacy network packet parser that has been failing. The original Python script used to process custom binary packets and calculate a statistical convergence metric, but it was lost. All we have left is an old screenshot of the protocol specification and convergence formula, attached to the ticket at `/app/ticket_attachment.png`.

Recently, a junior dev tried to rewrite it but their script crashed with the following stack trace:
```
Traceback (most recent call last):
  File "old_parser.py", line 24, in <module>
    y_val = solve_newton(X)
  File "old_parser.py", line 15, in solve_newton
    y = y - (y**3 + X*y - 1) / (3*y**2 + X)
ZeroDivisionError: float division by zero
```

We need you to write a robust Python script at `/home/user/parser.py` that takes a single hexadecimal string as a command-line argument (representing exactly 10 bytes of packet payload), parses it according to the specification in `/app/ticket_attachment.png`, applies the convergence formula to find the value (handling the division by zero edge case safely as per the spec), and prints the resulting JSON to standard output. 

There is a reference compiled binary of the parser available at `/app/oracle_parser`. Our automated CI will verify your script by passing thousands of random hex strings to both `/app/oracle_parser` and your script (`python3 /home/user/parser.py`), and asserting that their standard outputs match exactly byte-for-byte. 

Please analyze the image, implement the parser, and fix the convergence failure!