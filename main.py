from flask import Flask, request, jsonify
import json


app = Flask(__name__)


def read_users_from_file():
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def write_users_to_file(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)


users = read_users_from_file()


@app.route('/')
def home():
    return "Welcome to the User Management System API."


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = len(users) + 1
    user = {
        'id': user_id,
        'name': data.get('name'),
        'email': data.get('email')
    }
    users.append(user)
    write_users_to_file(users)
    return jsonify(user), 201


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user), 200


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    write_users_to_file(users)
    return jsonify(user), 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user['id'] != user_id]
    write_users_to_file(users)
    return jsonify({'message': 'User deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)
