As a build engineer, you are responsible for maintaining a legacy artifact processing tool. The tool is written in Go and evaluates mathematically encoded build configurations.

Currently, the processor is incomplete. It needs to decode a custom artifact format and act as a Reverse Polish Notation (RPN) interpreter.

In `/home/user/workspace`, you will find two files:
1. `artifact.txt` - Contains a single line of encoded artifact data.
2. `processor.go` - A partially written Go program that is supposed to process the artifact.

Your task is to:
1. Fix `processor.go` so that it correctly reads `/home/user/workspace/artifact.txt`.
2. The encoding scheme applied to the artifact is as follows: 
   - First, every character in the artifact string has had its ASCII value shifted by +1 (e.g., 'A' became 'B'). You must reverse this shift (subtract 1).
   - Second, decode the resulting string using standard Base64.
3. The resulting decoded string is a space-separated RPN (Reverse Polish Notation) mathematical expression containing integers and the operators `ADD`, `SUB`, `MUL`, and `DIV`.
4. Implement the RPN evaluation logic in `processor.go`. Note: for `SUB` and `DIV`, the first popped element is the right operand, and the second popped element is the left operand (e.g., `A B SUB` is `A - B`).
5. Run your Go program to evaluate the artifact and write the final integer result to `/home/user/workspace/output.txt`.
6. Once your script works, create a unified diff patch file of your changes to `processor.go` compared to its original state. Save this patch to `/home/user/workspace/fix.patch`.

Do not change the name of `processor.go`. Make sure `output.txt` contains exactly the numerical result and nothing else.