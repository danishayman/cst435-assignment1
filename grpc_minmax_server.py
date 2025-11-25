import grpc
from concurrent import futures
import time
import numpy as np
import matrix_pb2
import matrix_pb2_grpc
import argparse


class MatrixMinMaxServicer(matrix_pb2_grpc.MatrixMinMaxServicer):
    def FindMinMax(self, request, context):
        start_time = time.time()
        
        # Convert proto matrices to numpy arrays
        matrix_a = np.array([[val for val in row.values] for row in request.matrix_a])
        matrix_b = np.array([[val for val in row.values] for row in request.matrix_b])
        
        # Find min and max values
        min_a = float(np.min(matrix_a))
        max_a = float(np.max(matrix_a))
        min_b = float(np.min(matrix_b))
        max_b = float(np.max(matrix_b))
        
        computation_time = time.time() - start_time
        
        # Create response
        response = matrix_pb2.MinMaxResponse()
        response.min_a = min_a
        response.max_a = max_a
        response.min_b = min_b
        response.max_b = max_b
        response.computation_time = computation_time
        
        return response


def serve(port=50053):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    matrix_pb2_grpc.add_MatrixMinMaxServicer_to_server(
        MatrixMinMaxServicer(), server
    )
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"MinMax Service - gRPC Server started on port {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gRPC Matrix MinMax Server')
    parser.add_argument('--port', type=int, default=50053, help='Server port')
    args = parser.parse_args()
    serve(args.port)
