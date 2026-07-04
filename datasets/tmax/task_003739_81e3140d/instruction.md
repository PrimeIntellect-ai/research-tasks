You are a Machine Learning Engineer preparing training data and an inference API for a new recommendation pipeline.

We have received a specification document as an image located at `/app/spec.png`. 
Your task is to build a full data processing and serving pipeline that does the following:

1. **Extract Specifications**: 
   Use OCR (e.g., `tesseract`) to extract the text from `/app/spec.png`. The text contains the required hidden layer sizes for a neural network, as well as the target mean and standard deviation for a synthetic feature.

2. **Generate Synthetic Data**:
   Write a Python script to generate a synthetic dataset. 
   - Set the random seed to exactly `42` (using `numpy.random.seed(42)`).
   - Generate `1000` samples. 
   - The first 20 features should be drawn from a continuous uniform distribution over `[0, 1)`.
   - Append a 21st feature (index 20) drawn from a normal distribution using the `mean` and `standard deviation` extracted from the image. 

3. **Reconstruct Model Architecture**:
   Build a PyTorch Multi-Layer Perceptron (MLP). 
   - The input dimension is 21.
   - The hidden layers must exactly match the sizes extracted from the image, in order. Each hidden layer must be followed by a `ReLU` activation.
   - The output dimension must be 10 (no activation after the final output layer).
   - Before initializing the model weights, set `torch.manual_seed(42)`. Use standard default PyTorch linear layer initializations.
   - Pass the entire generated dataset (1000 samples) through the model to obtain the activations of the **last hidden layer** (the layer immediately preceding the final 10-dimensional output layer). 

4. **Serve the API**:
   Create and run a FastAPI or Flask web server listening on `127.0.0.1:8000`.
   Implement the following two endpoints:
   
   - `GET /recommend?item_id=<int>`
     Given a row index `item_id` (0 to 999), compute the cosine similarity between this item's last-hidden-layer activation and all other items' last-hidden-layer activations. 
     Return a JSON array of the top 5 most similar `item_id`s (excluding the queried item itself) in descending order of similarity. Example format: `{"similar_items": [12, 45, 99, 102, 5]}`.
     
   - `GET /stats`
     Perform a two-sided 1-sample t-test on the generated 21st feature (the normally distributed one) to test the null hypothesis that its population mean is equal to `0.0`. 
     Return the p-value and the 95% confidence interval for the sample mean (using standard t-distribution critical values). 
     Example format: `{"p_value": 0.0001, "ci_lower": 2.45, "ci_upper": 2.55}`.

Leave the web server running in the background or foreground so we can verify the endpoints.