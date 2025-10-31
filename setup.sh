#!/bin/bash

echo "Setting up Matrix Multiplication Service..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Generate gRPC code from proto file
echo "Generating gRPC code..."
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. matrix.proto

echo ""
echo "Setup complete!"
echo ""
echo "You can now:"
echo "1. Run single gRPC server: python grpc_server.py"
echo "2. Run single HTTP server: python http_server.py"
echo "3. Run gRPC client: python grpc_client.py --server localhost:50051"
echo "4. Run HTTP client: python http_client.py --server http://localhost:5000"
echo ""
echo "For Docker deployments:"
echo "- Single gRPC: docker-compose -f docker-compose-grpc-single.yml up"
echo "- Multi gRPC: docker-compose -f docker-compose-grpc-multi.yml up"
echo "- Single HTTP: docker-compose -f docker-compose-http-single.yml up"
echo "- Multi HTTP: docker-compose -f docker-compose-http-multi.yml up"
