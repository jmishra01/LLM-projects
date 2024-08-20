# LLM-projects

## Write Fibonacci series using Ollama library
```text

>>> python3 write-fib-series.py -h
usage: write-fib-series.py [-h] [-f F] [-l L] [-m M]

options:
  -h, --help  show this help message and exit
  -f F        Print content with JSON response received from LLM model.
  -l L        Pass programming lang name.
  -m M        Pass LLM model name.

>>> python3 write-fib-series -l Rust

Here's an implementation of the Fibonacci series in Rust:
```
```Rust
 fn fibonacci(n: u32) -> Vec<u32> {
     let mut result = vec![0, 1];

     if n <= 1 {
         return result[..n as usize].to_vec();
     }

     for i in 2..n {
         let next = result[i-1] + result[i-2];
         result.push(next);
     }

     result
 }

 fn main() {
     let fib_series = fibonacci(10);
     println!("{:?}", fib_series);
 }
```
```text
This code defines a function fibonacci that takes an integer n as input and returns the first n numbers in the Fibonacci series. The function initializes a vector with the first two Fibonacci numbers, 0 and 1. If n is less than or equal to 1, it simply returns the initial
vector.

For larger values of n, it enters a loop where it calculates each subsequent Fibonacci number as the sum of the previous two, and appends this number to the result vector.

The main function demonstrates how to use this fibonacci function by calculating the first 10 Fibonacci numbers and printing them out.
```
