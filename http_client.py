import requests
import numpy as np
import time
import argparse


def create_random_matrix(rows: int, cols: int) -> np.ndarray:
    """Create a random matrix with given dimensions."""
    return np.random.rand(rows, cols)


def run_client(server_url: str, matrix_size: int, num_requests: int):
    """Run the HTTP client and send matrix multiplication requests."""
    total_time = 0
    server_computation_time = 0
    
    print(f"Sending {num_requests} requests to {server_url}")
    print(f"Matrix size: {matrix_size}x{matrix_size}")
    
    for i in range(num_requests):
        # Create random matrices
        matrix_a = create_random_matrix(matrix_size, matrix_size)
        matrix_b = create_random_matrix(matrix_size, matrix_size)
        
        # Prepare request data
        data = {
            'matrix_a': matrix_a.tolist(),
            'matrix_b': matrix_b.tolist()
        }
        
        # Send request and measure time
        start_time = time.time()
        try:
            response = requests.post(f"{server_url}/multiply", json=data)
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                total_time += elapsed_time
                server_computation_time += result['computation_time']
                
                print(f"Request {i+1}/{num_requests}: Total time = {elapsed_time:.4f}s, "
                      f"Server computation = {result['computation_time']:.4f}s")
            else:
                print(f"Request {i+1} failed with status {response.status_code}")
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
    
    avg_total_time = total_time / num_requests
    avg_server_time = server_computation_time / num_requests
    avg_network_time = (total_time - server_computation_time) / num_requests
    
    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)
    print(f"Total requests: {num_requests}")
    print(f"Matrix size: {matrix_size}x{matrix_size}")
    print(f"Average total time: {avg_total_time:.4f}s")
    print(f"Average server computation time: {avg_server_time:.4f}s")
    print(f"Average network overhead: {avg_network_time:.4f}s")
    print(f"Total time for all requests: {total_time:.4f}s")
    print("="*60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP Matrix Multiplication Client')
    parser.add_argument('--server', type=str, default='http://localhost:5000', 
                        help='Server URL')
    parser.add_argument('--size', type=int, default=50, 
                        help='Matrix size (NxN)')
    parser.add_argument('--requests', type=int, default=10, 
                        help='Number of requests to send')
    
    args = parser.parse_args()
    run_client(args.server, args.size, args.requests)
