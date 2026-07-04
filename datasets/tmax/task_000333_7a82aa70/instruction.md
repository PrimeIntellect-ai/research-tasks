You are assisting a data science researcher in organizing and scoring their datasets. The researcher has lost the original source code for their data scoring model, but they have a scanned image of the model's architecture and weights saved at `/app/model_specs.png`.

Your task is to reconstruct this model and implement a fast inference CLI tool in Go.

Requirements:
1. **Extract the Model:** Use whatever tools you need (e.g., `tesseract` is installed) to read the mathematical formula and neural network weights from `/app/model_specs.png`. The image describes how to combine two input features (`A` and `B`) to produce a final `Score`.
2. **Implement in Go:** Write a Go program that reads from standard input (`stdin`). 
    - The input will consist of multiple lines.
    - Each line will contain exactly two space-separated floating-point numbers representing feature `A` and feature `B` respectively (e.g., `1.2 -3.4`).
3. **Output Format:** For each input line, your program must compute the `Score` according to the exact architecture extracted from the image. Print the resulting score to standard output (`stdout`), formatted to exactly 4 decimal places (e.g., `0.5432`), followed by a newline.
4. **Build the Binary:** Compile your Go program and save the final executable exactly at `/home/user/scorer`.

Make sure your binary is executable and strictly adheres to the input/output formats, as it will be heavily tested against automated data streams. Do not print any extra debugging text to standard output.