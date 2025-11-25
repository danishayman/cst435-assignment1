import grpc
from concurrent import futures
import time
import numpy as np
import matrix_pb2
import matrix_pb2_grpc
import argparse


class MatrixMultiplicationServicer(matrix_pb2_grpc.MatrixMultiplicationServicer):
    def Multiply(self, request, context):
        start_time = time.time()
        
        # Convert proto matrices to numpy arrays
        matrix_a = np.array([[val for val in row.values] for row in request.matrix_a])
        matrix_b = np.array([[val for val in row.values] for row in request.matrix_b])
        
        # Perform matrix multiplication
        result = np.matmul(matrix_a, matrix_b)
        
        computation_time = time.time() - start_time
        
        # Convert result back to proto format
        response = matrix_pb2.MatrixResponse()
        for row in result:
            matrix_row = response.result.add()
            matrix_row.values.extend(row)
        response.computation_time = computation_time
        
        return response


def serve(port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    matrix_pb2_grpc.add_MatrixMultiplicationServicer_to_server(
        MatrixMultiplicationServicer(), server
    )
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Multiplication Service - gRPC Server started on port {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gRPC Matrix Multiplication Server')
    parser.add_argument('--port', type=int, default=50051, help='Server port')
    args = parser.parse_args()
    serve(args.port)
