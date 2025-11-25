import grpc
import numpy as np
import time
import matrix_pb2
import matrix_pb2_grpc
import argparse
from typing import List


def create_random_matrix(rows: int, cols: int) -> np.ndarray:
    """Create a random matrix with given dimensions."""
    return np.random.rand(rows, cols)


def numpy_to_proto_matrix(matrix: np.ndarray) -> List:
    """Convert numpy array to proto matrix format."""
    proto_rows = []
    for row in matrix:
        proto_row = matrix_pb2.MatrixRow()
        proto_row.values.extend(row)
        proto_rows.append(proto_row)
    return proto_rows


def run_microservices_client(multiply_addr: str, average_addr: str, minmax_addr: str, 
                              matrix_size: int, num_requests: int):
    """Run the gRPC client and send requests to separate microservices."""
    
    # Create separate channels for each service
    multiply_channel = grpc.insecure_channel(multiply_addr)
    average_channel = grpc.insecure_channel(average_addr)
    minmax_channel = grpc.insecure_channel(minmax_addr)
    
    # Create stubs for each service
    multiply_stub = matrix_pb2_grpc.MatrixMultiplicationStub(multiply_channel)
    average_stub = matrix_pb2_grpc.MatrixAverageStub(average_channel)
    minmax_stub = matrix_pb2_grpc.MatrixMinMaxStub(minmax_channel)
    
    # Timing accumulators for each service
    total_multiply_time = 0
    total_average_time = 0
    total_minmax_time = 0
    
    server_multiply_time = 0
    server_average_time = 0
    server_minmax_time = 0
    
    print(f"Sending {num_requests} requests to MICROSERVICES")
    print(f"  Multiply service: {multiply_addr}")
    print(f"  Average service: {average_addr}")
    print(f"  MinMax service: {minmax_addr}")
    print(f"Matrix size: {matrix_size}x{matrix_size}")
    print("="*70)
    
    for i in range(num_requests):
        # Create random matrices
        matrix_a = create_random_matrix(matrix_size, matrix_size)
        matrix_b = create_random_matrix(matrix_size, matrix_size)
        
        # Convert to proto format
        request = matrix_pb2.MatrixRequest()
        request.matrix_a.extend(numpy_to_proto_matrix(matrix_a))
        request.matrix_b.extend(numpy_to_proto_matrix(matrix_b))
        
        # Service 1: Matrix Multiplication
        start_time = time.time()
        try:
            response = multiply_stub.Multiply(request)
            multiply_elapsed = time.time() - start_time
            total_multiply_time += multiply_elapsed
            server_multiply_time += response.computation_time
        except grpc.RpcError as e:
            print(f"Request {i+1} - Multiply failed: {e}")
            multiply_elapsed = 0
        
        # Service 2: Average Calculation
        start_time = time.time()
        try:
            response = average_stub.CalculateAverage(request)
            average_elapsed = time.time() - start_time
            total_average_time += average_elapsed
            server_average_time += response.computation_time
        except grpc.RpcError as e:
            print(f"Request {i+1} - Average failed: {e}")
            average_elapsed = 0
        
        # Service 3: MinMax Finding
        start_time = time.time()
        try:
            response = minmax_stub.FindMinMax(request)
            minmax_elapsed = time.time() - start_time
            total_minmax_time += minmax_elapsed
            server_minmax_time += response.computation_time
        except grpc.RpcError as e:
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
    
    # Close channels
    multiply_channel.close()
    average_channel.close()
    minmax_channel.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gRPC Microservices Client')
    parser.add_argument('--multiply', type=str, default='localhost:50051', 
                        help='Multiply service address (host:port)')
    parser.add_argument('--average', type=str, default='localhost:50052', 
                        help='Average service address (host:port)')
    parser.add_argument('--minmax', type=str, default='localhost:50053', 
                        help='MinMax service address (host:port)')
    parser.add_argument('--size', type=int, default=50, 
                        help='Matrix size (NxN)')
    parser.add_argument('--requests', type=int, default=10, 
                        help='Number of requests to send')
    
    args = parser.parse_args()
    run_microservices_client(args.multiply, args.average, args.minmax, args.size, args.requests)
