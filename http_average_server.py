from flask import Flask, request, jsonify
import numpy as np
import time
import argparse

app = Flask(__name__)


@app.route('/average', methods=['POST'])
def average():
    """Handle matrix average calculation request."""
    start_time = time.time()
    
    data = request.json
    
    # Convert to numpy arrays
    matrix_a = np.array(data['matrix_a'])
    matrix_b = np.array(data['matrix_b'])
    
    # Calculate averages
    average_a = float(np.mean(matrix_a))
    average_b = float(np.mean(matrix_b))
    
    computation_time = time.time() - start_time
    
    # Return result
    return jsonify({
        'average_a': average_a,
        'average_b': average_b,
        'computation_time': computation_time
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'average'})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP Matrix Average Server')
    parser.add_argument('--port', type=int, default=5002, help='Server port')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Server host')
    args = parser.parse_args()
    
    print(f"Average Service - HTTP Server starting on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, threaded=True)
