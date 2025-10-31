#!/usr/bin/env python3
"""
Benchmark script to compare all 4 configurations:
1. Single container gRPC
2. Multi-container gRPC
3. Single container HTTP
4. Multi-container HTTP
"""

import subprocess
import time
import argparse
import json


def run_benchmark(client_type, server_address, matrix_size, num_requests):
    """Run a benchmark for a specific configuration."""
    print(f"\n{'='*70}")
    print(f"Running {client_type} benchmark")
    print(f"Server: {server_address}, Matrix: {matrix_size}x{matrix_size}, Requests: {num_requests}")
    print(f"{'='*70}\n")
    
    if client_type == 'grpc':
        cmd = [
            'python', 'grpc_client.py',
            '--server', server_address,
            '--size', str(matrix_size),
            '--requests', str(num_requests)
        ]
    else:  # http
        cmd = [
            'python', 'http_client.py',
            '--server', server_address,
            '--size', str(matrix_size),
            '--requests', str(num_requests)
        ]
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    end_time = time.time()
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    return end_time - start_time


def main():
    parser = argparse.ArgumentParser(description='Benchmark Matrix Multiplication Service')
    parser.add_argument('--size', type=int, default=50, help='Matrix size (NxN)')
    parser.add_argument('--requests', type=int, default=20, help='Number of requests per test')
    args = parser.parse_args()
    
    configurations = [
        ('grpc', 'Single gRPC', 'localhost:50051'),
        ('grpc', 'Multi gRPC Worker 1', 'localhost:50051'),
        ('grpc', 'Multi gRPC Worker 2', 'localhost:50052'),
        ('grpc', 'Multi gRPC Worker 3', 'localhost:50053'),
        ('http', 'Single HTTP', 'http://localhost:5000'),
        ('http', 'Multi HTTP Worker 1', 'http://localhost:5001'),
        ('http', 'Multi HTTP Worker 2', 'http://localhost:5002'),
        ('http', 'Multi HTTP Worker 3', 'http://localhost:5003'),
    ]
    
    results = {}
    
    print("\n" + "="*70)
    print("MATRIX MULTIPLICATION SERVICE BENCHMARK")
    print("="*70)
    print(f"Matrix Size: {args.size}x{args.size}")
    print(f"Requests per configuration: {args.requests}")
    print("="*70)
    
    for client_type, name, server in configurations:
        try:
            total_time = run_benchmark(client_type, server, args.size, args.requests)
            results[name] = total_time
            time.sleep(2)  # Brief pause between tests
        except Exception as e:
            print(f"Failed to run {name}: {e}")
            results[name] = None
    
    # Print summary
    print("\n" + "="*70)
    print("BENCHMARK SUMMARY")
    print("="*70)
    for name, total_time in results.items():
        if total_time:
            print(f"{name:30s}: {total_time:.4f}s")
        else:
            print(f"{name:30s}: FAILED")
    print("="*70)


if __name__ == '__main__':
    main()
