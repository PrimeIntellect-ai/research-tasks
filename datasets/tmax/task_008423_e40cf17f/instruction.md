I am a performance engineer profiling a spectroscopy data analysis application. The current numerical integration component is extremely slow because it uses a naive uniform grid with 10^8 points to integrate absorption peaks. 

I need you to write a more efficient Rust program that models a Lorentzian absorption peak and extracts key metrics using a much smaller grid with a higher-order method.

The absorption peak is modeled by the function:
`f(x) = 15.0 / ((x - 12.0)^2 + 0.04)`

Write a Rust program in `/home/user/integrate.rs` that performs the following tasks:
1. Calculates the numerical integral of `f(x)` from `x = 0.0` to `x = 24.0` using **Simpson's 1/3 rule** with exactly `N = 1000` subintervals (which means 1001 evaluation points).
2. Analytically or numerically finds the two points (`x1` and `x2`, where `x1 < x2`) where the intensity drops to exactly `f(x) = 100.0`.

Your Rust program should write the results to a JSON file at `/home/user/report.json` with the following format. Round all numeric values to exactly **4 decimal places**.

Expected JSON format:
```json
{
  "integral": 123.4567,
  "x1": 1.2345,
  "x2": 2.3456
}
```

You must compile and run your Rust program so that the `report.json` file is generated. You can use standard Rust (`rustc`) to compile the file.