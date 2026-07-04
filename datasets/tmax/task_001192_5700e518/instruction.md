You are assisting a data researcher in setting up a feature engineering pipeline for a new dataset. The researcher has left the schema and linear algebra transformation rules in an image artifact. 

Your task involves setting up the environment, extracting the transformation rules, and implementing a highly optimized C++ pipeline step that conforms strictly to the schema.

Step 1: Extract Transformation Rules
An image containing the dataset's linear transformation weights, bias, and schema constraints is located at `/app/transformation_rules.png`. You must use OCR (tesseract is preinstalled) to extract the text. The image contains:
- A 2x3 Weight Matrix (W) under the header "Weights:"
- A 1x2 Bias vector (B) under the header "Bias:"
- Min and Max clamping values under the header "Clamp:"

Step 2: Implement the Feature Engineering Binary
Write a C++ program at `/home/user/transform.cpp` and compile it to `/home/user/transform`.
The program must:
1. Read exactly three `double` precision floating-point numbers from `stdin` (representing the 3x1 input feature vector $X$).
2. Compute the new 2x1 feature vector $Y$ using the linear algebra formula: $Y = W \times X + B$.
3. Enforce the data schema: clamp both output values of $Y$ strictly to the minimum and maximum values extracted from the "Clamp:" section of the image.
4. Print the two resulting clamped values to `stdout`, separated by a single space, formatted to exactly 4 decimal places (e.g., `1.2345 -4.5670`). Print a newline at the end.

Constraints:
- You may install any necessary C++ libraries (e.g., Eigen3) or write the math operations from scratch.
- The compiled binary must be located exactly at `/home/user/transform` and be executable.
- The program should process one set of 3 floats per execution.