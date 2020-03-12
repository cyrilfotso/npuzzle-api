from flask import Flask, request, jsonify
from flask_cors import CORS

from State import State
from implementation import a_star_search, ida_star_search

# Define the WSGI application object
app = Flask(__name__)
app.url_map.strict_slashes = False


# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'msg': '404.html'}), 404


# welcome page
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the n-puzzle engine api'})


@app.route('/a_star', methods=['POST'])
def a_star_solve():
    data = request.get_json()
    try:
        size = data.get('size', 3)
        config = data.get('config', [])
        type_heuristic = data.get('type_heuristic', 2)
        goal_mode = data.get('goal_mode', 'zero_first')
        print('ida', config)
        state = State(config=tuple(config), type_heuristic=type_heuristic,
                      parent=None, goal_mode=goal_mode, moves=0, size=size, from_dir='')
        out = a_star_search(state)
        if out[0]:
            return jsonify({'found': out[0], 'actions_list': out[4],
                            'Depth': out[6], 'Search_time': out[5]})
        else:
            jsonify({'found': out[0]}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 401


@app.route('/ida_star', methods=['POST'])
def ida_star_solve():
    data = request.get_json()
    try:
        size = data.get('size', 3)
        config = data.get('config', [])
        type_heuristic = data.get('type_heuristic', 2)
        goal_mode = data.get('goal_mode', 'zero_first')
        print('ida', config, type_heuristic, goal_mode)
        state = State(config=tuple(config), type_heuristic=type_heuristic,
                      parent=None, goal_mode=goal_mode, moves=0, size=size, from_dir='')
        out = ida_star_search(state)
        if out[0]:
            return jsonify({'found': out[0], 'actions_list': out[3],
                            'Depth': out[4], 'Search_time': out[5]})
        else:
            jsonify({'found': False}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 401


CORS(app)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
