#from flask import Flask, request, jsonify
#import logging
#
#app = Flask(__name__)
#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)
#
#@app.route('/api/hello', methods=['GET'])
#def say_hello():
#    """
#    A simple endpoint that returns a greeting.
#
#   """ logger.info("Hello endpoint was reached!")
#    
#    return jsonify({
#        'message': 'Hello Niko'
#    }), 200
#    
#@app.errorhandler(404)
#def not_found(error):
#   return jsonify({'error': 'Resource not found'}), 404
#
#@app.errorhandler(500)
#def internal_error(error):
#    logger.error(f"Internal error: {error}")
#    return jsonify({'error': 'Internal server error'}), 500
#
#if __name__ == '__main__':
#    app.run(debug=True, port=5001)  

from flask import Flask, request, jsonify
import logging
import random

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

allowed_names = ["Niko", "Promit"]

@app.route('/api/hello', methods=['GET'])
def say_hello():
    """
    Greets a random name from the allowed_names list.
    If the list is empty, it gives a fallback greeting.
    """
    if not allowed_names:
        return jsonify({'message': 'Hello world! No names are currently registered.'}), 200
        
    random_name = random.choice(allowed_names)
    logger.info(f"Greeting picked: {random_name}")
    
    return jsonify({
        'message': f'Hello {random_name}',
        'current_pool': allowed_names
    }), 200

@app.route('/api/names', methods=['POST'])
def add_name():
    """
    Adds a new name to the list.
    Expects JSON: {"name": "YourName"}
    """
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing "name" field in request body'}), 400
        
    new_name = data['name'].strip()
    
    if not new_name:
        return jsonify({'error': 'Name cannot be empty'}), 400
        
    if new_name in allowed_names:
        return jsonify({'message': f'{new_name} is already in the list!', 'names': allowed_names}), 200

    allowed_names.append(new_name)
    logger.info(f"Added name: {new_name}")
    
    return jsonify({
        'message': f'Successfully added {new_name}',
        'names': allowed_names
    }), 201

@app.route('/api/names', methods=['DELETE'])
def delete_name():
    """
    Deletes a name from the list.
    Expects JSON: {"name": "YourName"}
    """
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing "name" field in request body'}), 400
        
    target_name = data['name'].strip()
    
    if target_name in allowed_names:
        allowed_names.remove(target_name)
        logger.info(f"Deleted name: {target_name}")
        return jsonify({
            'message': f'Successfully deleted {target_name}',
            'names': allowed_names
        }), 200
    else:
        return jsonify({'error': f'Name "{target_name}" not found in the list.'}), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    
