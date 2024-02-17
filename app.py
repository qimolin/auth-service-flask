import os
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from jwt_utils import create_jwt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/authDatabase"
mongo = PyMongo(app)

secretKey = os.getenv("JWT_SECRET_KEY")

@app.post('/users')
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if mongo.db.users.find_one({"username": username}):
        return jsonify({"error": "Duplicate username"}), 409

    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')

    mongo.db.users.insert_one({
        "username": username,
        "password": encrypted_password
    })

    return jsonify({"message": "User registered successfully"}), 201

@app.put('/users')
def update_password():
    # TODO: Implement password update
    pass

@app.post('/users/login')
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # get user from DB
    user = mongo.db.users.find_one({"username": username})

    if user:
        if bcrypt.check_password_hash(user['password'], password):
            token = create_jwt(str(user['_id']), secretKey)
            return jsonify({"token": token}), 200  # Return the JWT token
        else:
            return jsonify({"error": "Forbidden"}), 403
    else:
        return jsonify({"error": "Forbidden"}), 403

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)