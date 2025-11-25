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


def serve(port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    matrix_pb2_grpc.add_MatrixMultiplicationServicer_to_server(
        MatrixMultiplicationServicer(), server
    )
    matrix_pb2_grpc.add_MatrixAverageServicer_to_server(
        MatrixAverageServicer(), server
    )
    matrix_pb2_grpc.add_MatrixMinMaxServicer_to_server(
        MatrixMinMaxServicer(), server
    )
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"gRPC Server started on port {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gRPC Matrix Multiplication Server')
    parser.add_argument('--port', type=int, default=50051, help='Server port')
    args = parser.parse_args()
    serve(args.port)
