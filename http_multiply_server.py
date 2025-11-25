from flask import Flask, request, jsonify
import numpy as np
import time
import argparse

app = Flask(__name__)


@app.route('/multiply', methods=['POST'])
def multiply():
    """Handle matrix multiplication request."""
    start_time = time.time()
    
    data = request.json
    
    # Convert to numpy arrays
    matrix_a = np.array(data['matrix_a'])
    matrix_b = np.array(data['matrix_b'])
    
    # Perform matrix multiplication
    result = np.matmul(matrix_a, matrix_b)
    
    computation_time = time.time() - start_time
    
    # Return result
    return jsonify({
        'result': result.tolist(),
        'computation_time': computation_time
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'multiply'})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP Matrix Multiplication Server')
    parser.add_argument('--port', type=int, default=5001, help='Server port')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Server host')
    args = parser.parse_args()
    
    print(f"Multiplication Service - HTTP Server starting on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, threaded=True)
