#!/usr/bin/env python3
"""
Multi-container performance benchmark script.
This script demonstrates the advantage of multi-container setups by sending
concurrent requests and comparing performance.
"""

import subprocess
import time
import argparse
import concurrent.futures
import statistics


def run_single_request(client_type, server_address, matrix_size):
    """Run a single request and return the time taken."""
    if client_type == 'grpc':
        cmd = [
            'python', 'grpc_client.py',
            '--server', server_address,
            '--size', str(matrix_size),
            '--requests', '1'
        ]
    else:  # http
        cmd = [
            'python', 'http_client.py',
            '--server', server_address,
            '--size', str(matrix_size),
            '--requests', '1'
        ]
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    end_time = time.time()
    
    return end_time - start_time


def test_single_container(client_type, server_address, matrix_size, num_requests):
    """Test single container by sending requests sequentially."""
    print(f"\n{'='*70}")
    print(f"Testing SINGLE Container - {client_type.upper()}")
    print(f"Server: {server_address}")
    print(f"Matrix: {matrix_size}x{matrix_size}, Requests: {num_requests}")
    print(f"{'='*70}")
    
    times = []
    start_time = time.time()
    
    for i in range(num_requests):
        request_time = run_single_request(client_type, server_address, matrix_size)
        times.append(request_time)
        print(f"Request {i+1}/{num_requests}: {request_time:.4f}s")
    
    total_time = time.time() - start_time
    
    print(f"\nResults:")
    print(f"  Total time: {total_time:.4f}s")
    print(f"  Average per request: {statistics.mean(times):.4f}s")
    print(f"  Min: {min(times):.4f}s, Max: {max(times):.4f}s")
    
    return total_time, times


def test_multi_container_sequential(client_type, server_addresses, matrix_size, num_requests):
    """Test multiple containers by distributing requests sequentially (round-robin)."""
    print(f"\n{'='*70}")
    print(f"Testing MULTI Container (Sequential) - {client_type.upper()}")
    print(f"Servers: {', '.join(server_addresses)}")
    print(f"Matrix: {matrix_size}x{matrix_size}, Requests: {num_requests}")
    print(f"{'='*70}")
    
    times = []
    start_time = time.time()
    
    for i in range(num_requests):
        # Round-robin across servers
        server = server_addresses[i % len(server_addresses)]
        request_time = run_single_request(client_type, server, matrix_size)
        times.append(request_time)
        print(f"Request {i+1}/{num_requests} to {server}: {request_time:.4f}s")
    
    total_time = time.time() - start_time
    
    print(f"\nResults:")
    print(f"  Total time: {total_time:.4f}s")
    print(f"  Average per request: {statistics.mean(times):.4f}s")
    print(f"  Min: {min(times):.4f}s, Max: {max(times):.4f}s")
    
    return total_time, times


def test_multi_container_parallel(client_type, server_addresses, matrix_size, num_requests):
    """Test multiple containers by sending requests in parallel (TRUE BENEFIT)."""
    print(f"\n{'='*70}")
    print(f"Testing MULTI Container (PARALLEL) - {client_type.upper()}")
    print(f"Servers: {', '.join(server_addresses)}")
    print(f"Matrix: {matrix_size}x{matrix_size}, Concurrent Requests: {num_requests}")
    print(f"{'='*70}")
    
    start_time = time.time()
    
    # Send requests in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(server_addresses)) as executor:
        # Create a list of futures
        futures = []
        for i in range(num_requests):
            server = server_addresses[i % len(server_addresses)]
            future = executor.submit(run_single_request, client_type, server, matrix_size)
            futures.append((i+1, server, future))
        
        # Wait for all to complete and collect results
        times = []
        for req_num, server, future in futures:
            request_time = future.result()
            times.append(request_time)
            print(f"Request {req_num}/{num_requests} to {server}: {request_time:.4f}s")
    
    total_time = time.time() - start_time
    
    print(f"\nResults:")
    print(f"  Total time (wall clock): {total_time:.4f}s")
    print(f"  Average per request: {statistics.mean(times):.4f}s")
    print(f"  Min: {min(times):.4f}s, Max: {max(times):.4f}s")
    print(f"  Speedup: {sum(times)/total_time:.2f}x")
    
    return total_time, times


def main():
    parser = argparse.ArgumentParser(description='Benchmark Multi-Container Performance')
    parser.add_argument('--size', type=int, default=100, help='Matrix size (NxN)')
    parser.add_argument('--requests', type=int, default=12, help='Number of requests')
    parser.add_argument('--type', type=str, choices=['grpc', 'http', 'both'], default='both',
                        help='Which protocol to test')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("MULTI-CONTAINER PERFORMANCE BENCHMARK")
    print("="*70)
    print(f"Matrix Size: {args.size}x{args.size}")
    print(f"Total Requests: {args.requests}")
    print("="*70)
    
    results = {}
    
    # Test gRPC
    if args.type in ['grpc', 'both']:
        print("\n" + "="*70)
        print("gRPC PERFORMANCE TESTS")
        print("="*70)
        
        # Single container
        single_time, _ = test_single_container(
            'grpc', 'localhost:50051', args.size, args.requests
        )
        results['gRPC Single'] = single_time
        
        time.sleep(2)
        
        # Multi container - Sequential
        multi_seq_time, _ = test_multi_container_sequential(
            'grpc',
            ['localhost:50051', 'localhost:50052', 'localhost:50053'],
            args.size,
            args.requests
        )
        results['gRPC Multi (Sequential)'] = multi_seq_time
        
        time.sleep(2)
        
        # Multi container - Parallel (THE TRUE BENEFIT!)
        multi_par_time, _ = test_multi_container_parallel(
            'grpc',
            ['localhost:50051', 'localhost:50052', 'localhost:50053'],
            args.size,
            args.requests
        )
        results['gRPC Multi (Parallel)'] = multi_par_time
    
    # Test HTTP
    if args.type in ['http', 'both']:
        print("\n" + "="*70)
        print("HTTP PERFORMANCE TESTS")
        print("="*70)
        
        # Single container
        single_time, _ = test_single_container(
            'http', 'http://localhost:5000', args.size, args.requests
        )
        results['HTTP Single'] = single_time
        
        time.sleep(2)
        
        # Multi container - Sequential
        multi_seq_time, _ = test_multi_container_sequential(
            'http',
            ['http://localhost:5001', 'http://localhost:5002', 'http://localhost:5003'],
            args.size,
            args.requests
        )
        results['HTTP Multi (Sequential)'] = multi_seq_time
        
        time.sleep(2)
        
        # Multi container - Parallel (THE TRUE BENEFIT!)
        multi_par_time, _ = test_multi_container_parallel(
            'http',
            ['http://localhost:5001', 'http://localhost:5002', 'http://localhost:5003'],
            args.size,
            args.requests
        )
        results['HTTP Multi (Parallel)'] = multi_par_time
    
    # Print final summary
    print("\n" + "="*70)
    print("FINAL COMPARISON SUMMARY")
    print("="*70)
    for name, total_time in results.items():
        print(f"{name:30s}: {total_time:.4f}s")
    print("="*70)
    
    # Calculate speedups
    if args.type == 'grpc' or args.type == 'both':
        if 'gRPC Single' in results and 'gRPC Multi (Parallel)' in results:
            speedup = results['gRPC Single'] / results['gRPC Multi (Parallel)']
            print(f"\ngRPC Parallel Speedup: {speedup:.2f}x")
    
    if args.type == 'http' or args.type == 'both':
        if 'HTTP Single' in results and 'HTTP Multi (Parallel)' in results:
            speedup = results['HTTP Single'] / results['HTTP Multi (Parallel)']
            print(f"HTTP Parallel Speedup: {speedup:.2f}x")
    
    print("\n" + "="*70)
    print("KEY INSIGHT:")
    print("The 'Parallel' tests show the TRUE benefit of multi-container setups!")
    print("Multiple containers can handle concurrent requests simultaneously,")
    print("significantly reducing total wall-clock time.")
    print("="*70)


if __name__ == '__main__':
    main()
