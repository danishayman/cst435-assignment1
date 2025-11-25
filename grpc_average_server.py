import grpc
from concurrent import futures
import time
import numpy as np
import matrix_pb2
import matrix_pb2_grpc
import argparse


class MatrixAverageServicer(matrix_pb2_grpc.MatrixAverageServicer):
    def CalculateAverage(self, request, context):
        start_time = time.time()
        
        # Convert proto matrices to numpy arrays
        matrix_a = np.array([[val for val in row.values] for row in request.matrix_a])
        matrix_b = np.array([[val for val in row.values] for row in request.matrix_b])
        
        # Calculate averages
        average_a = float(np.mean(matrix_a))
        average_b = float(np.mean(matrix_b))
        
        computation_time = time.time() - start_time
        
        # Create response
        response = matrix_pb2.AverageResponse()
        response.average_a = average_a
        response.average_b = average_b
        response.computation_time = computation_time
        
        return response


def serve(port=50052):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    matrix_pb2_grpc.add_MatrixAverageServicer_to_server(
        MatrixAverageServicer(), server
    )
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Average Service - gRPC Server started on port {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gRPC Matrix Average Server')
    parser.add_argument('--port', type=int, default=50052, help='Server port')
    args = parser.parse_args()
    serve(args.port)
