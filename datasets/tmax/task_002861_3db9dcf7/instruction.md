You are an engineer working on the backend for a new web-based calculator tool. The product manager has provided a voice memo detailing the business logic and constraints for a custom expression evaluator. 

Your task is to:
1. Extract the requirements from the audio file located at `/app/memo.wav`. You may use tools like `espeak`, `pocketsphinx`, or any available Python library to transcribe or understand the audio if you cannot listen to it directly.
2. Build an expression evaluator in Python that implements the Reverse Polish Notation (RPN) logic and specific constraints requested by the product manager. 
3. Write your implementation to `/home/user/rpn_eval.py`. The script must take exactly one command-line argument (a string representing the expression) and print the evaluated result to standard output.
4. Implement rigorous error handling: if an expression is malformed, causes division by zero, lacks sufficient operands, or leaves more than one value on the evaluation stack at the end, your program must output exactly `ERROR`.
5. Write your own unit tests to ensure your program complies strictly with the logic described in the audio memo. 

Your code should be robust, as it will be rigorously tested against a large number of randomly generated edge cases to ensure exact equivalence with a hidden reference implementation.

Expected usage:
`python3 /home/user/rpn_eval.py "10 5 / MIN 5"`