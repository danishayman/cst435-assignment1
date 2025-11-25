import requests
import numpy as np
import time
import argparse


def create_random_matrix(rows: int, cols: int) -> np.ndarray:
    """Create a random matrix with given dimensions."""
    return np.random.rand(rows, cols)


def run_microservices_client(multiply_url: str, average_url: str, minmax_url: str,
                              matrix_size: int, num_requests: int):
    """Run the HTTP client and send requests to separate microservices."""
    
    # Timing accumulators for each service
    total_multiply_time = 0
    total_average_time = 0
    total_minmax_time = 0
    
    server_multiply_time = 0
    server_average_time = 0
    server_minmax_time = 0
    
    print(f"Sending {num_requests} requests to MICROSERVICES")
    print(f"  Multiply service: {multiply_url}")
    print(f"  Average service: {average_url}")
    print(f"  MinMax service: {minmax_url}")
    print(f"Matrix size: {matrix_size}x{matrix_size}")
    print("="*70)
    
    for i in range(num_requests):
        # Create random matrices
        matrix_a = create_random_matrix(matrix_size, matrix_size)
        matrix_b = create_random_matrix(matrix_size, matrix_size)
        
        # Prepare request data
        data = {
            'matrix_a': matrix_a.tolist(),
            'matrix_b': matrix_b.tolist()
        }
        
        # Service 1: Matrix Multiplication
        start_time = time.time()
        try:
            response = requests.post(f"{multiply_url}/multiply", json=data)
            multiply_elapsed = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                total_multiply_time += multiply_elapsed
                server_multiply_time += result['computation_time']
            else:
                print(f"Request {i+1} - Multiply failed with status {response.status_code}")
                multiply_elapsed = 0
        except Exception as e:
            print(f"Request {i+1} - Multiply failed: {e}")
            multiply_elapsed = 0
        
        # Service 2: Average Calculation
        start_time = time.time()
        try:
            response = requests.post(f"{average_url}/average", json=data)
            average_elapsed = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                total_average_time += average_elapsed
                server_average_time += result['computation_time']
            else:
                print(f"Request {i+1} - Average failed with status {response.status_code}")
                average_elapsed = 0
        except Exception as e:
            print(f"Request {i+1} - Average failed: {e}")
            average_elapsed = 0
        
        # Service 3: MinMax Finding
        start_time = time.time()
        try:
            response = requests.post(f"{minmax_url}/minmax", json=data)
            minmax_elapsed = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                total_minmax_time += minmax_elapsed
                server_minmax_time += result['computation_time']
            else:
                print(f"Request {i+1} - MinMax failed with status {response.status_code}")
                minmax_elapsed = 0
        except Exception as e:
            print(f"Request {i+1} - MinMax failed: {e}")
            minmax_elapsed = 0
        
        # Calculate total time for this request iteration
        request_total = multiply_elapsed + average_elapsed + minmax_elapsed
        
        print(f"Request {i+1}/{num_requests}: Total={request_total:.4f}s "
              f"[Multiply={multiply_elapsed:.4f}s, Average={average_elapsed:.4f}s, MinMax={minmax_elapsed:.4f}s]")
    
    # Calculate overall totals and averages
    grand_total_time = total_multiply_time + total_average_time + total_minmax_time
    avg_multiply_time = total_multiply_time / num_requests
    avg_average_time = total_average_time / num_requests
    avg_minmax_time = total_minmax_time / num_requests
    avg_total_time = grand_total_time / num_requests
    
    avg_server_multiply = server_multiply_time / num_requests
    avg_server_average = server_average_time / num_requests
    avg_server_minmax = server_minmax_time / num_requests
    avg_server_total = (server_multiply_time + server_average_time + server_minmax_time) / num_requests
    
    total_network_overhead = grand_total_time - (server_multiply_time + server_average_time + server_minmax_time)
    avg_network_overhead = total_network_overhead / num_requests
    
    print("\n" + "="*70)
    print("MICROSERVICES RESULTS - 3 SEPARATE CONTAINERS")
    print("="*70)
    print(f"Total requests: {num_requests}")
    print(f"Matrix size: {matrix_size}x{matrix_size}")
    print()
    print("PER SERVICE AVERAGES:")
    print(f"  Multiply  - Avg total: {avg_multiply_time:.4f}s, Avg server: {avg_server_multiply:.4f}s")
    print(f"  Average   - Avg total: {avg_average_time:.4f}s, Avg server: {avg_server_average:.4f}s")
    print(f"  MinMax    - Avg total: {avg_minmax_time:.4f}s, Avg server: {avg_server_minmax:.4f}s")
    print()
    print("COMBINED TOTALS:")
    print(f"  Average total time per request (all 3 services): {avg_total_time:.4f}s")
    print(f"  Average server computation per request: {avg_server_total:.4f}s")
    print(f"  Average network overhead per request: {avg_network_overhead:.4f}s")
    print()
    print(f"  GRAND TOTAL TIME (all {num_requests} requests × 3 services): {grand_total_time:.4f}s")
    print(f"  Total server computation: {server_multiply_time + server_average_time + server_minmax_time:.4f}s")
    print(f"  Total network overhead: {total_network_overhead:.4f}s")
    print("="*70)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP Microservices Client')
    parser.add_argument('--multiply', type=str, default='http://localhost:5001', 
                        help='Multiply service URL')
    parser.add_argument('--average', type=str, default='http://localhost:5002', 
                        help='Average service URL')
    parser.add_argument('--minmax', type=str, default='http://localhost:5003', 
                        help='MinMax service URL')
    parser.add_argument('--size', type=int, default=50, 
                        help='Matrix size (NxN)')
    parser.add_argument('--requests', type=int, default=10, 
                        help='Number of requests to send')
    
    args = parser.parse_args()
    run_microservices_client(args.multiply, args.average, args.minmax, args.size, args.requests)
